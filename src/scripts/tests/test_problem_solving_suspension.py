from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from test_sync_problem_solving import COLLECTION, FakeProblemSupabase
from problem_solving_suspension import suspension_action, RequestError
from problem_solving_bookmark import bookmark_action
from problem_solving_card import card_action
from problem_solving_store import ProblemSolvingStore, problem_collection
from problem_solving_stats import problem_solving_stats
from record_problem_solving_rating import record_problem_rating
from select_problem_solving_card import select_problem
from sync_problem_solving import sync_problem_solving


class SuspensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / 'state.sqlite3'
        self.request = {'collection_directory': str(COLLECTION), 'database_path': str(self.database)}
        self.key = problem_collection(str(COLLECTION))[1]
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def action(self, action, problem_id='problem-2'):
        return suspension_action({**self.request, 'action': action, 'problem_id': problem_id}, self.now)

    def test_unseen_selection_and_restore(self):
        first = select_problem(self.request, self.now)['problem']['id']
        self.action('suspend', first)
        self.assertNotEqual(select_problem(self.request, self.now)['problem']['id'], first)
        stats = problem_solving_stats(self.request, self.now)['collection_state']
        self.assertEqual(stats['suspended'], 1)
        self.assertEqual(stats['total'], len(problem_collection(str(COLLECTION))[2]) - 1)
        listed = suspension_action({**self.request, 'action': 'list'})['suspended']
        self.assertEqual(listed[0]['problem_id'], first)
        self.assertTrue(Path(listed[0]['brief_path']).is_file())
        self.action('restore', first)
        self.assertEqual(select_problem(self.request, self.now)['problem']['id'], first)
        self.assertEqual(ProblemSolvingStore(self.database).cards_for_collection(self.key), {})
        with self.assertRaises(RequestError):
            self.action('suspend', 'unknown')

    def test_bookmarks_artifacts_and_schedule_survive(self):
        request = {**self.request, 'problem_id': 'problem-2'}
        card_action({**request, 'action': 'reveal'})
        record_problem_rating({**request, 'final_rating': 'good',
            'solve_duration_ms': 10, 'discussion_duration_ms': 20}, self.now)
        bookmark_action({**request, 'action': 'create', 'note': 'keep this note'}, self.now)
        store = ProblemSolvingStore(self.database)
        before = store.cards_for_collection(self.key)['problem-2'].to_json()
        artifact = store.artifact(self.key, 'problem-2')
        self.action('suspend')
        self.assertEqual(store.list_bookmarks(self.key), [])
        self.assertEqual(store.open_bookmark_ids(self.key), set())
        with self.assertRaises(ValueError):
            card_action({**request, 'action': 'get'})
        self.action('restore')
        self.assertEqual(store.cards_for_collection(self.key)['problem-2'].to_json(), before)
        self.assertEqual(store.artifact(self.key, 'problem-2'), artifact)
        self.assertEqual(store.list_bookmarks(self.key)[0]['note'], 'keep this note')

    def test_suspended_overdue_card_is_excluded_and_restored(self):
        request = {**self.request, 'problem_id': 'problem-2'}
        card_action({**request, 'action': 'reveal'})
        record_problem_rating({**request, 'final_rating': 'good',
            'solve_duration_ms': 10, 'discussion_duration_ms': 20}, self.now)
        later = datetime(2026, 2, 1, tzinfo=timezone.utc)
        self.assertEqual(select_problem(self.request, later)['problem']['id'], 'problem-2')
        self.action('suspend')
        stats = problem_solving_stats(self.request, later)
        self.assertEqual(stats['today']['due_now'], 0)
        self.assertEqual(stats['collection_state']['introduced'], 0)
        self.assertEqual(stats['reviews']['total'], 1)
        self.assertNotEqual(select_problem(self.request, later)['problem']['id'], 'problem-2')
        self.action('restore')
        self.assertEqual(select_problem(self.request, later)['problem']['id'], 'problem-2')

    @patch.dict('os.environ', {'PROBLEM_SOLVING_SUPABASE_KEY': 'fake-key'})
    def test_sync_suspend_restore_and_idempotence(self):
        other = Path(self.temp.name) / 'other.sqlite3'
        remote = FakeProblemSupabase()
        def sync(database):
            return sync_problem_solving({**self.request, 'database_path': str(database),
                'supabase_url': 'https://example.supabase.co'}, remote)
        self.action('suspend')
        self.assertEqual(sync(self.database)['status'], 'success')
        self.assertEqual(sync(other)['downloaded']['suspension'], 1)
        self.assertIn('problem-2', ProblemSolvingStore(other).suspensions(self.key))
        suspension_action({**self.request, 'database_path': str(other),
            'action': 'restore', 'problem_id': 'problem-2'}, self.now)
        sync(other)
        sync(self.database)
        self.assertEqual(ProblemSolvingStore(self.database).suspensions(self.key), {})
        self.assertEqual(sync(self.database)['downloaded']['suspension'], 0)
