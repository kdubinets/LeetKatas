from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parents[1]
COLLECTION = (
    REPOSITORY_ROOT
    / "practice"
    / "problem_solving"
    / "collections"
    / "algorithmic_problem_solving"
)
COLLECTION_ORDER = tuple(
    problem_id
    for problem_id in (COLLECTION / "problem_order.md").read_text(encoding="utf-8").splitlines()
    if problem_id
)
sys.path.insert(0, str(SCRIPTS))

from practice_scheduler import PracticeStore, SchedulerError  # noqa: E402
from problem_solving_bookmark import bookmark_action  # noqa: E402
from problem_solving_card import card_action  # noqa: E402
from problem_solving_stats import problem_solving_stats  # noqa: E402
from problem_solving_store import ProblemSolvingStore  # noqa: E402
from record_problem_solving_rating import record_problem_rating  # noqa: E402
from select_problem_solving_card import select_problem  # noqa: E402


class ProblemSolvingWorkflowTests(unittest.TestCase):
    def request(self, database: Path, **values) -> dict:
        return {
            "collection_directory": str(COLLECTION),
            "database_path": str(database),
            **values,
        }

    def run_script(self, name: str, request: dict) -> tuple[int, dict]:
        result = subprocess.run(
            ["python3", str(SCRIPTS / name)],
            input=json.dumps(request),
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_commands_preserve_json_protocol_through_a_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database)
            code, selected = self.run_script("select_problem_solving_card.py", request)
            self.assertEqual(code, 0)
            self.assertEqual(selected["problem"]["id"], "problem-2")
            code, revealed = self.run_script(
                "problem_solving_card.py",
                {**request, "problem_id": "problem-2", "action": "reveal"},
            )
            self.assertEqual(code, 0)
            self.assertIn("solution_outline", revealed)
            code, rated = self.run_script(
                "record_problem_solving_rating.py",
                {
                    **request,
                    "problem_id": "problem-2",
                    "final_rating": "good",
                    "solve_duration_ms": 1,
                    "discussion_duration_ms": 1,
                },
            )
            self.assertEqual(code, 0)
            self.assertTrue(rated["recorded"])
            code, stats = self.run_script("problem_solving_stats.py", request)
            self.assertEqual(code, 0)
            self.assertEqual(stats["reviews"]["total"], 1)

    def test_schema_coexists_with_existing_practice_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            connection = PracticeStore(database).connect()
            connection.execute(
                "INSERT INTO schema_metadata(key, value) VALUES ('test_marker', 'preserved')"
            )
            connection.commit()
            connection.close()

            ProblemSolvingStore(database).connect().close()

            with sqlite3.connect(database) as connection:
                self.assertEqual(
                    connection.execute(
                        "SELECT value FROM schema_metadata WHERE key='test_marker'"
                    ).fetchone()[0],
                    "preserved",
                )
                self.assertIsNotNone(
                    connection.execute(
                        "SELECT 1 FROM sqlite_master WHERE name='problem_solving_reviews'"
                    ).fetchone()
                )

    def test_selection_bookmark_lifecycle_and_private_note(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database)
            self.assertEqual(select_problem(request)["problem"]["id"], "problem-2")

            created = bookmark_action(
                {**request, "action": "create", "problem_id": "problem-2", "note": "think later"},
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
            self.assertTrue(created["bookmarked"])
            self.assertEqual(created["revision"], 1)
            self.assertEqual(select_problem(request)["problem"]["id"], "problem-4")
            bookmarks = bookmark_action({**request, "action": "list"})["bookmarks"]
            self.assertEqual(bookmarks[0]["note"], "think later")

            removed = bookmark_action(
                {**request, "action": "remove", "problem_id": "problem-2"},
                datetime(2026, 1, 2, tzinfo=timezone.utc),
            )
            self.assertFalse(removed["bookmarked"])
            self.assertEqual(removed["revision"], 2)
            self.assertEqual(bookmark_action({**request, "action": "list"}), {"bookmarks": []})
            self.assertEqual(select_problem(request)["problem"]["id"], "problem-2")

    def test_hint_reveal_rating_gate_and_statistics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database, problem_id="problem-2")
            with self.assertRaisesRegex(SchedulerError, "only after"):
                record_problem_rating(
                    {
                        **request,
                        "final_rating": "good",
                        "solve_duration_ms": 100,
                        "discussion_duration_ms": 20,
                    }
                )

            hinted = card_action({**request, "action": "hint"})
            self.assertIn("hint", hinted)
            self.assertNotIn("solution_outline", hinted)
            card_action({**request, "action": "clarification"})
            revealed = card_action({**request, "action": "reveal"})
            self.assertIn("solution_outline", revealed)
            recorded = record_problem_rating(
                {
                    **request,
                    "final_rating": "acceptable",
                    "solve_duration_ms": 100,
                    "discussion_duration_ms": 20,
                },
                datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
            self.assertTrue(recorded["recorded"])
            self.assertFalse(recorded["bookmark_retained"])
            self.assertIsNone(ProblemSolvingStore(database).artifact(
                "leetkatas.problem_solving.initial_seed", "problem-2"
            ))

            same_day_stats = problem_solving_stats(
                self.request(database), datetime(2026, 1, 1, tzinfo=timezone.utc)
            )
            self.assertEqual(same_day_stats["today"]["reviews"], 1)
            self.assertEqual(same_day_stats["today"]["new_reviewed"], 1)
            self.assertEqual(same_day_stats["today"]["ratings"]["acceptable"], 1)
            self.assertEqual(same_day_stats["today"]["practice_time_ms"], 120)
            self.assertEqual(len(same_day_stats["forecast"]["days"]), 7)
            self.assertEqual(same_day_stats["history"][0]["date"], "2026-01-01")

            stats = problem_solving_stats(
                self.request(database), datetime(2030, 1, 1, tzinfo=timezone.utc)
            )
            self.assertEqual(stats["reviews"]["total"], 1)
            self.assertEqual(stats["reviews"]["problems_total"], 1)
            self.assertEqual(stats["reviews"]["hint_used"], 1)
            self.assertEqual(stats["reviews"]["clarification_used"], 1)
            self.assertEqual(stats["reviews"]["revealed"], 1)
            self.assertEqual(stats["reviews"]["revealed_unrated"], 0)
            self.assertEqual(stats["reviews"]["ratings"]["acceptable"], 1)
            self.assertEqual(stats["collection_state"]["due_now"], 1)
            self.assertEqual(stats["today"]["reviews"], 0)
            self.assertEqual(stats["today"]["new_reviewed"], 0)
            self.assertEqual(stats["today"]["due_later_today"], 0)
            self.assertEqual(
                select_problem(
                    self.request(database), datetime(2030, 1, 1, tzinfo=timezone.utc)
                )["problem"]["id"],
                "problem-2",
            )

    def test_rating_does_not_remove_an_open_bookmark(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database, problem_id="problem-2")
            bookmark_action({**request, "action": "create"})
            card_action({**request, "action": "reveal"})

            recorded = record_problem_rating(
                {
                    **request,
                    "final_rating": "good",
                    "solve_duration_ms": 1,
                    "discussion_duration_ms": 2,
                }
            )

            self.assertTrue(recorded["bookmark_retained"])
            self.assertEqual(
                bookmark_action({**request, "action": "list"})["bookmarks"][0]["problem_id"],
                "problem-2",
            )
            self.assertEqual(select_problem(self.request(database))["problem"]["id"], "problem-4")

    def test_clearing_revealed_bookmark_preserves_rating_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database, problem_id="problem-2")
            bookmark_action({**request, "action": "create"})
            card_action({**request, "action": "reveal"})
            bookmark_action({**request, "action": "remove"})

            recorded = record_problem_rating(
                {
                    **request,
                    "final_rating": "good",
                    "solve_duration_ms": 1,
                    "discussion_duration_ms": 2,
                }
            )

            self.assertTrue(recorded["recorded"])
            self.assertFalse(recorded["bookmark_retained"])

    def test_rating_retains_selection_and_reveal_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            selected_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
            revealed_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
            request = self.request(database, problem_id="problem-2")
            select_problem(self.request(database), selected_at)
            ProblemSolvingStore(database).update_artifact(
                "leetkatas.problem_solving.initial_seed",
                "problem-2",
                revealed=True,
                updated_at=revealed_at,
            )

            record_problem_rating(
                {
                    **request,
                    "final_rating": "good",
                    "solve_duration_ms": 1,
                    "discussion_duration_ms": 2,
                },
                datetime(2026, 1, 3, tzinfo=timezone.utc),
            )

            with sqlite3.connect(database) as connection:
                row = connection.execute(
                    "SELECT selected_at, revealed_at FROM problem_solving_reviews"
                ).fetchone()
            self.assertEqual(row, (selected_at.isoformat(), revealed_at.isoformat()))

    def test_schema_version_one_migrates_without_losing_reviews(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            with sqlite3.connect(database) as connection:
                connection.executescript(
                    """
                    CREATE TABLE schema_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    INSERT INTO schema_metadata VALUES ('problem_solving_schema_version', '1');
                    CREATE TABLE problem_solving_reviews (
                      review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      event_id TEXT NOT NULL UNIQUE,
                      collection_key TEXT NOT NULL,
                      problem_id TEXT NOT NULL,
                      review_datetime TEXT NOT NULL,
                      final_rating TEXT NOT NULL,
                      review_log_json TEXT NOT NULL,
                      hint_used INTEGER NOT NULL,
                      clarification_used INTEGER NOT NULL,
                      gave_up INTEGER NOT NULL,
                      solve_duration_ms INTEGER NOT NULL,
                      discussion_duration_ms INTEGER NOT NULL,
                      remote_confirmed INTEGER NOT NULL DEFAULT 0
                    );
                    INSERT INTO problem_solving_reviews (
                      event_id, collection_key, problem_id, review_datetime,
                      final_rating, review_log_json, hint_used, clarification_used,
                      gave_up, solve_duration_ms, discussion_duration_ms
                    ) VALUES ('event', 'collection', 'problem-1',
                      '2026-01-01T00:00:00+00:00', 'good', '{}', 0, 0, 0, 1, 2);
                    """
                )

            ProblemSolvingStore(database).connect().close()

            with sqlite3.connect(database) as connection:
                columns = {
                    row[1] for row in connection.execute(
                        "PRAGMA table_info(problem_solving_reviews)"
                    )
                }
                version = connection.execute(
                    "SELECT value FROM schema_metadata "
                    "WHERE key='problem_solving_schema_version'"
                ).fetchone()[0]
                count = connection.execute(
                    "SELECT count(*) FROM problem_solving_reviews"
                ).fetchone()[0]
            self.assertEqual(version, "3")
            self.assertEqual(count, 1)
            self.assertIn("selected_at", columns)
            self.assertIn("revealed_at", columns)
            self.assertNotIn("gave_up", columns)

    def test_no_due_response_after_every_problem_is_introduced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            reviewed_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
            for problem_id in COLLECTION_ORDER:
                request = self.request(database, problem_id=problem_id)
                card_action({**request, "action": "reveal"})
                record_problem_rating(
                    {
                        **request,
                        "final_rating": "good",
                        "solve_duration_ms": 1,
                        "discussion_duration_ms": 1,
                    },
                    reviewed_at,
                )

            response = select_problem(self.request(database), reviewed_at)

            self.assertIsNone(response["problem"])
            self.assertIsNotNone(response["next_due"])


if __name__ == "__main__":
    unittest.main()
