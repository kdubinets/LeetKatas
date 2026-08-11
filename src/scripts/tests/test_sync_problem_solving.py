from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parents[1]
COLLECTION = (
    REPOSITORY_ROOT
    / "practice"
    / "problem_solving"
    / "collections"
    / "algorithmic_problem_solving"
)
sys.path.insert(0, str(SCRIPTS))

from problem_solving_bookmark import bookmark_action  # noqa: E402
from problem_solving_card import card_action  # noqa: E402
from problem_solving_store import ProblemSolvingStore  # noqa: E402
from record_problem_solving_rating import record_problem_rating  # noqa: E402
from sync_problem_solving import sync_problem_solving  # noqa: E402


class FakeProblemSupabase:
    def __init__(self, events=None):
        self.events = {
            "problem_solving_review_events": [],
            "problem_solving_bookmark_events": [],
            "problem_solving_artifact_events": [],
        }
        self.next_sequence = {table: 1 for table in self.events}
        for table, values in (events or {}).items():
            for value in values:
                event = dict(value)
                event.setdefault("sync_sequence", self.next_sequence[table])
                self.next_sequence[table] = max(
                    self.next_sequence[table], event["sync_sequence"] + 1
                )
                self.events[table].append(event)
        self.calls = []

    def request(self, method, url, headers, body):
        self.calls.append((method, url, headers, body))
        table = url.split("/rest/v1/", 1)[1].split("?", 1)[0]
        if method == "GET":
            query = dict(item.split("=", 1) for item in url.split("?", 1)[1].split("&"))
            cursor = int(query["sync_sequence"].removeprefix("gt."))
            limit = int(query["limit"])
            page = sorted(
                (
                    event for event in self.events[table]
                    if event["sync_sequence"] > cursor
                ),
                key=lambda event: event["sync_sequence"],
            )[:limit]
            return 200, json.dumps(page).encode()
        known = {event["event_id"] for event in self.events[table]}
        for value in json.loads(body):
            if value["event_id"] in known:
                continue
            event = dict(value)
            event["sync_sequence"] = self.next_sequence[table]
            self.next_sequence[table] += 1
            self.events[table].append(event)
            known.add(event["event_id"])
        return 201, b""


class ProblemSolvingSyncTests(unittest.TestCase):
    def request(self, database: Path, **values) -> dict:
        return {
            "collection_directory": str(COLLECTION),
            "database_path": str(database),
            "supabase_url": "https://example.supabase.co",
            **values,
        }

    def make_review(self, database: Path, bookmarked=False) -> None:
        request = self.request(database, problem_id="problem-2")
        if bookmarked:
            bookmark_action({**request, "action": "create", "note": "private note"})
        card_action({**request, "action": "hint"})
        ProblemSolvingStore(database).update_artifact(
            "leetkatas.problem_solving.initial_seed",
            "problem-2",
            conversation_history=[
                {"role": "user", "content": "private question"},
                {"role": "assistant", "content": "private answer"},
            ],
        )
        card_action({**request, "action": "reveal"})
        record_problem_rating(
            {
                **request,
                "final_rating": "good",
                "solve_duration_ms": 10,
                "discussion_duration_ms": 20,
            },
            datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

    def synchronize(self, request, fake):
        with patch.dict(os.environ, {"PROBLEM_SOLVING_SUPABASE_KEY": "secret"}):
            return sync_problem_solving(request, fake)

    def test_default_sync_excludes_private_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            self.make_review(database, bookmarked=True)
            fake = FakeProblemSupabase()

            response = self.synchronize(self.request(database), fake)

            self.assertEqual(response["status"], "success")
            self.assertEqual(len(fake.events["problem_solving_review_events"]), 1)
            self.assertEqual(len(fake.events["problem_solving_bookmark_events"]), 1)
            self.assertEqual(fake.events["problem_solving_artifact_events"], [])
            serialized = json.dumps(fake.events)
            self.assertNotIn("private note", serialized)
            self.assertNotIn("private question", serialized)
            self.assertNotIn("solution_outline", serialized)

    def test_private_sync_is_explicit_and_plaintext(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            self.make_review(database, bookmarked=True)
            fake = FakeProblemSupabase()

            response = self.synchronize(
                self.request(database, private_content_sync=True), fake
            )

            self.assertEqual(response["status"], "success")
            artifacts = fake.events["problem_solving_artifact_events"]
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0]["artifact_json"]["note"], "private note")
            self.assertTrue(artifacts[0]["artifact_json"]["revealed"])
            self.assertEqual(
                artifacts[0]["artifact_json"]["conversation_history"][0]["content"],
                "private question",
            )

    def test_repeated_sync_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            self.make_review(database)
            fake = FakeProblemSupabase()
            request = self.request(database)

            first = self.synchronize(request, fake)
            second = self.synchronize(request, fake)

            self.assertEqual(first["uploaded"]["review"], 1)
            self.assertEqual(second["uploaded"]["review"], 0)
            self.assertEqual(second["downloaded"]["review"], 0)
            self.assertEqual(len(fake.events["problem_solving_review_events"]), 1)

    def test_fresh_database_downloads_reviews_and_rebuilds_fsrs_card(self) -> None:
        event = {
            "event_id": str(uuid.uuid4()),
            "collection_id": "leetkatas.problem_solving.initial_seed",
            "problem_id": "problem-4",
            "review_datetime": "2026-01-01T00:00:00+00:00",
            "final_rating": "acceptable",
            "hint_used": False,
            "clarification_used": False,
            "solve_duration_ms": 10,
            "discussion_duration_ms": 20,
        }
        fake = FakeProblemSupabase({"problem_solving_review_events": [event]})
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "fresh.sqlite3"

            response = self.synchronize(self.request(database), fake)

            self.assertEqual(response["downloaded"]["review"], 1)
            with sqlite3.connect(database) as connection:
                self.assertEqual(
                    connection.execute("SELECT count(*) FROM problem_solving_reviews").fetchone()[0],
                    1,
                )
                self.assertEqual(
                    connection.execute("SELECT count(*) FROM problem_solving_cards").fetchone()[0],
                    1,
                )

    def test_same_revision_bookmark_conflict_uses_time_then_event_id(self) -> None:
        remote_event = {
            "event_id": str(uuid.uuid4()),
            "collection_id": "leetkatas.problem_solving.initial_seed",
            "problem_id": "problem-2",
            "revision": 1,
            "action": "remove",
            "event_datetime": "2026-01-02T00:00:00+00:00",
        }
        fake = FakeProblemSupabase({"problem_solving_bookmark_events": [remote_event]})
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            bookmark_action(
                {**self.request(database), "action": "create", "problem_id": "problem-2"},
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            )

            response = self.synchronize(self.request(database), fake)

            self.assertEqual(response["downloaded"]["bookmark"], 1)
            self.assertEqual(
                bookmark_action({**self.request(database), "action": "list"}),
                {"bookmarks": []},
            )

    def test_private_artifact_restores_on_fresh_database(self) -> None:
        event = {
            "event_id": str(uuid.uuid4()),
            "collection_id": "leetkatas.problem_solving.initial_seed",
            "problem_id": "problem-8",
            "revision": 3,
            "updated_at": "2026-01-03T00:00:00+00:00",
            "artifact_json": {
                "hint_requested": True,
                "clarification_used": False,
                "revealed": False,
                "selected_at": "2026-01-01T00:00:00+00:00",
                "revealed_at": None,
                "note": "restored note",
                "conversation_history": [],
            },
        }
        fake = FakeProblemSupabase({"problem_solving_artifact_events": [event]})
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "fresh.sqlite3"

            response = self.synchronize(
                self.request(database, private_content_sync=True), fake
            )

            self.assertEqual(response["downloaded"]["artifact"], 1)
            restored = card_action(
                {**self.request(database), "problem_id": "problem-8", "action": "get"}
            )
            self.assertEqual(restored["state"]["note"], "restored note")
            self.assertIn("hint", restored)

    def test_rated_unbookmarked_artifact_is_not_restored(self) -> None:
        review = {
            "event_id": str(uuid.uuid4()),
            "collection_id": "leetkatas.problem_solving.initial_seed",
            "problem_id": "problem-8",
            "review_datetime": "2026-01-03T00:00:00+00:00",
            "final_rating": "good",
            "hint_used": True,
            "clarification_used": False,
            "solve_duration_ms": 10,
            "discussion_duration_ms": 20,
        }
        artifact = {
            "event_id": str(uuid.uuid4()),
            "collection_id": "leetkatas.problem_solving.initial_seed",
            "problem_id": "problem-8",
            "revision": 2,
            "updated_at": "2026-01-02T00:00:00+00:00",
            "artifact_json": {
                "hint_requested": True,
                "clarification_used": False,
                "revealed": True,
                "selected_at": "2026-01-01T00:00:00+00:00",
                "revealed_at": "2026-01-02T00:00:00+00:00",
                "note": None,
                "conversation_history": [],
            },
        }
        fake = FakeProblemSupabase({
            "problem_solving_review_events": [review],
            "problem_solving_artifact_events": [artifact],
        })
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "fresh.sqlite3"

            response = self.synchronize(
                self.request(database, private_content_sync=True), fake
            )

            self.assertEqual(response["status"], "success")
            with sqlite3.connect(database) as connection:
                self.assertEqual(
                    connection.execute(
                        "SELECT count(*) FROM problem_solving_artifacts"
                    ).fetchone()[0],
                    0,
                )

    def test_unknown_remote_problem_is_rejected_without_partial_import(self) -> None:
        def review(problem_id):
            return {
                "event_id": str(uuid.uuid4()),
                "collection_id": "leetkatas.problem_solving.initial_seed",
                "problem_id": problem_id,
                "review_datetime": "2026-01-01T00:00:00+00:00",
                "final_rating": "good",
                "hint_used": False,
                "clarification_used": False,
                "solve_duration_ms": 1,
                "discussion_duration_ms": 1,
            }

        fake = FakeProblemSupabase({
            "problem_solving_review_events": [review("problem-2"), review("problem-999")]
        })
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "fresh.sqlite3"

            response = self.synchronize(self.request(database), fake)

            self.assertEqual(response["status"], "unavailable")
            with sqlite3.connect(database) as connection:
                self.assertEqual(
                    connection.execute("SELECT count(*) FROM problem_solving_reviews").fetchone()[0],
                    0,
                )


if __name__ == "__main__":
    unittest.main()
