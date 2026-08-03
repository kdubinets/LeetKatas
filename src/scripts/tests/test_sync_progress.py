from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from practice_scheduler import PracticeStore, collection_identity  # noqa: E402
from record_rating import record_rating  # noqa: E402
from sync_progress import UnavailableError, sync_progress  # noqa: E402


class FakeSupabase:
    def __init__(self, events=None, failure=None):
        self.events = list(events or [])
        self.failure = failure
        self.calls = []

    def request(self, method, url, headers, body):
        self.calls.append((method, url, headers, body))
        if self.failure:
            raise UnavailableError(self.failure)
        if method == "GET":
            query = dict(item.split("=", 1) for item in url.split("?", 1)[1].split("&"))
            offset = int(query["offset"])
            limit = int(query["limit"])
            return 200, json.dumps(self.events[offset : offset + limit]).encode()
        uploaded = json.loads(body)
        known = {event["event_id"] for event in self.events}
        self.events.extend(event for event in uploaded if event["event_id"] not in known)
        return 201, b""


class StaticResponse:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self.body = body

    def request(self, method, url, headers, body):
        return self.status, self.body


class SyncProgressTests(unittest.TestCase):
    def make_collection(self, root: Path, identity="test.cpp.collection") -> Path:
        collection = root / "collection"
        collection.mkdir()
        (collection / "collection.json").write_text(json.dumps({
            "schema_version": 1, "id": identity,
        }))
        (collection / "example.cpp").write_text("int solve() { return 1; }\n")
        (collection / "example.md").write_text("# Example\n")
        return collection

    def request(self, collection: Path, database: Path) -> dict:
        return {
            "exercise_directory": str(collection),
            "database_path": str(database),
            "supabase_url": "https://example.supabase.co",
        }

    def rating(self, collection: Path, database: Path, when=None, rating="good"):
        return record_rating({
            "exercise_directory": str(collection),
            "database_path": str(database),
            "exercise_id": "example",
            "compiled": True,
            "proposed_rating": "good",
            "final_rating": rating,
            "review_status": "available",
            "reviewer_name": "Fake",
            "reviewer_model": "model",
            "reviewer_reasoning_effort": "low",
            "review_attempts": 1,
            "solve_duration_ms": 10,
            "feedback_duration_ms": 20,
        }, when)

    def test_identity_is_portable_and_malformed_metadata_is_local_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection = self.make_collection(root)
            self.assertEqual(collection_identity(collection), "test.cpp.collection")
            (collection / "collection.json").write_text('{"schema_version":1,"id":"bad id"}')
            self.assertIsNone(collection_identity(collection))

    def test_v5_migration_assigns_uuid_without_losing_history_or_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection = root / "legacy_collection"
            collection.mkdir()
            (collection / "example.cpp").write_text("int solve() { return 1; }\n")
            (collection / "example.md").write_text("# Example\n")
            seed = root / "seed.sqlite3"
            request = {
                "exercise_directory": str(collection), "database_path": str(seed),
                "exercise_id": "example", "compiled": True,
                "proposed_rating": "good", "final_rating": "excellent",
                "review_status": "available", "reviewer_name": "Fake",
                "reviewer_model": "model", "reviewer_reasoning_effort": "low",
                "review_attempts": 2, "solve_duration_ms": 30,
                "feedback_duration_ms": 40, "submitted_source": "private source",
                "review_response": {"status": "available", "feedback": {"summary": "private"}},
            }
            record_rating(request, datetime(2026, 1, 1, tzinfo=timezone.utc))
            with sqlite3.connect(seed) as connection:
                card = connection.execute("SELECT * FROM cards").fetchone()
                review = connection.execute(
                    """SELECT collection_key,exercise_id,review_datetime,final_rating,
                       compiled,proposed_rating,review_status,reviewer_name,reviewer_model,
                       reviewer_reasoning_effort,review_attempts,solve_duration_ms,
                       feedback_duration_ms,review_log_json FROM reviews"""
                ).fetchone()
                artifact = connection.execute("SELECT * FROM review_artifacts").fetchone()

            legacy = root / "legacy.sqlite3"
            with sqlite3.connect(legacy) as connection:
                connection.executescript("""
                    CREATE TABLE schema_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    INSERT INTO schema_metadata VALUES ('schema_version', '5');
                    CREATE TABLE cards (
                      collection_key TEXT NOT NULL, exercise_id TEXT NOT NULL,
                      card_json TEXT NOT NULL, due_at TEXT NOT NULL, created_at TEXT NOT NULL,
                      updated_at TEXT NOT NULL, PRIMARY KEY(collection_key, exercise_id));
                    CREATE TABLE reviews (
                      review_id INTEGER PRIMARY KEY AUTOINCREMENT, collection_key TEXT NOT NULL,
                      exercise_id TEXT NOT NULL, review_datetime TEXT NOT NULL,
                      final_rating TEXT NOT NULL, compiled INTEGER NOT NULL,
                      proposed_rating TEXT, review_status TEXT NOT NULL, reviewer_name TEXT,
                      reviewer_model TEXT, reviewer_reasoning_effort TEXT,
                      review_attempts INTEGER NOT NULL, solve_duration_ms INTEGER,
                      feedback_duration_ms INTEGER, review_log_json TEXT NOT NULL,
                      FOREIGN KEY(collection_key,exercise_id) REFERENCES cards(collection_key,exercise_id));
                    CREATE TABLE review_artifacts (
                      review_id INTEGER PRIMARY KEY, created_at TEXT NOT NULL,
                      expires_at TEXT NOT NULL, submitted_source TEXT NOT NULL,
                      review_response_json TEXT NOT NULL,
                      FOREIGN KEY(review_id) REFERENCES reviews(review_id) ON DELETE CASCADE);
                """)
                connection.execute("INSERT INTO cards VALUES (?,?,?,?,?,?)", card)
                connection.execute(
                    """INSERT INTO reviews
                       (collection_key,exercise_id,review_datetime,final_rating,compiled,
                        proposed_rating,review_status,reviewer_name,reviewer_model,
                        reviewer_reasoning_effort,review_attempts,solve_duration_ms,
                        feedback_duration_ms,review_log_json)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", review
                )
                connection.execute("INSERT INTO review_artifacts VALUES (?,?,?,?,?)", artifact)

            migrated = PracticeStore(legacy).connect()
            try:
                stored_review = migrated.execute(
                    """SELECT collection_key,exercise_id,review_datetime,final_rating,
                       compiled,proposed_rating,review_status,reviewer_name,reviewer_model,
                       reviewer_reasoning_effort,review_attempts,solve_duration_ms,
                       feedback_duration_ms,review_log_json,event_id,remote_confirmed FROM reviews"""
                ).fetchone()
                stored_artifact = migrated.execute("SELECT * FROM review_artifacts").fetchone()
                version = migrated.execute(
                    "SELECT value FROM schema_metadata WHERE key='schema_version'"
                ).fetchone()[0]
            finally:
                migrated.close()
            self.assertEqual(tuple(stored_review[:14]), review)
            self.assertEqual(str(uuid.UUID(stored_review[14])), stored_review[14])
            self.assertEqual(stored_review[15], 0)
            self.assertEqual(tuple(stored_artifact), artifact)
            self.assertEqual(version, "6")

    def test_rating_creates_pending_uuid_and_upload_is_idempotent_and_private(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            self.rating(collection, database)
            with sqlite3.connect(database) as connection:
                event_id, confirmed = connection.execute(
                    "SELECT event_id, remote_confirmed FROM reviews"
                ).fetchone()
            self.assertEqual(len(event_id), 36)
            self.assertEqual(confirmed, 0)

            fake = FakeSupabase()
            first = sync_progress(self.request(collection, database), fake)
            second = sync_progress(self.request(collection, database), fake)
            self.assertEqual((first["uploaded"], second["uploaded"]), (1, 0))
            self.assertEqual(first["downloaded"], 0)
            post_body = next(body for method, _, _, body in fake.calls if method == "POST")
            post_headers = next(headers for method, _, headers, _ in fake.calls if method == "POST")
            encoded = post_body.decode()
            self.assertNotIn("secret-key", encoded)
            self.assertNotIn("submitted_source", encoded)
            self.assertNotIn('"feedback":', encoded)
            self.assertEqual(post_headers["apikey"], "secret-key")
            self.assertNotIn("Authorization", post_headers)
            with sqlite3.connect(database) as connection:
                self.assertEqual(connection.execute(
                    "SELECT remote_confirmed FROM reviews"
                ).fetchone()[0], 1)

    def test_network_failure_is_nonfatal_and_leaves_pending_event(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            self.rating(collection, database)
            response = sync_progress(
                self.request(collection, database), FakeSupabase(failure="network request failed")
            )
            self.assertEqual(response["status"], "unavailable")
            self.assertEqual(response["pending"], 1)
            self.assertNotIn("secret-key", json.dumps(response))

    def test_authentication_and_malformed_responses_are_sanitized_and_nonfatal(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            for name, adapter, expected in (
                ("auth", StaticResponse(401, b"private provider detail"), "authentication failed"),
                ("malformed", StaticResponse(200, b"not-json"), "malformed JSON"),
            ):
                database = root / f"{name}.sqlite3"
                self.rating(collection, database)
                response = sync_progress(self.request(collection, database), adapter)
                self.assertEqual(response["status"], "unavailable")
                self.assertEqual(response["pending"], 1)
                self.assertIn(expected, response["error"])
                self.assertNotIn("private provider detail", json.dumps(response))

    def test_invalid_remote_event_does_not_partially_import(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            invalid = {
                "event_id": "00000000-0000-4000-8000-000000000003",
                "collection_id": "test.cpp.collection", "exercise_id": "example",
                "review_datetime": datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat(),
                "final_rating": "good", "compiled": "not-a-boolean",
                "proposed_rating": None, "review_status": "available",
                "reviewer_name": None, "reviewer_model": None,
                "reviewer_reasoning_effort": None, "review_attempts": 0,
                "solve_duration_ms": None, "feedback_duration_ms": None,
            }
            response = sync_progress(self.request(collection, database), FakeSupabase([invalid]))
            self.assertEqual(response["status"], "unavailable")
            with sqlite3.connect(database) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM reviews").fetchone()[0], 0)
                self.assertEqual(connection.execute("SELECT count(*) FROM cards").fetchone()[0], 0)

    def test_download_pagination_and_upload_batching(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ), patch("sync_progress.PAGE_SIZE", 2), patch("sync_progress.UPLOAD_BATCH_SIZE", 1):
            root = Path(temporary)
            collection = self.make_collection(root)
            source_database = root / "source.sqlite3"
            start = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
            for offset, rating in enumerate(("fail", "acceptable", "good")):
                self.rating(collection, source_database, start + timedelta(days=offset), rating)
            fake = FakeSupabase()
            uploaded = sync_progress(self.request(collection, source_database), fake)
            self.assertEqual(uploaded["uploaded"], 3)
            self.assertEqual(sum(call[0] == "POST" for call in fake.calls), 3)

            restored = root / "restored.sqlite3"
            download_fake = FakeSupabase(fake.events)
            downloaded = sync_progress(self.request(collection, restored), download_fake)
            self.assertEqual(downloaded["downloaded"], 3)
            self.assertEqual(sum(call[0] == "GET" for call in download_fake.calls), 2)
            with sqlite3.connect(restored) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM reviews").fetchone()[0], 3)

    def test_fresh_database_downloads_and_reconstructs_card(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            source_database = root / "source.sqlite3"
            reviewed_at = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
            self.rating(collection, source_database, reviewed_at)
            source_fake = FakeSupabase()
            sync_progress(self.request(collection, source_database), source_fake)

            restored_database = root / "restored.sqlite3"
            response = sync_progress(
                self.request(collection, restored_database), FakeSupabase(source_fake.events)
            )
            self.assertEqual(response["downloaded"], 1)
            with sqlite3.connect(restored_database) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM reviews").fetchone()[0], 1)
                self.assertEqual(connection.execute("SELECT count(*) FROM cards").fetchone()[0], 1)

    def test_remote_histories_merge_chronologically_and_rebuild_card(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            first = datetime(2026, 1, 2, 12, tzinfo=timezone.utc)
            self.rating(collection, database, first, "good")
            fake = FakeSupabase()
            sync_progress(self.request(collection, database), fake)
            remote = dict(fake.events[0])
            remote["event_id"] = "00000000-0000-4000-8000-000000000001"
            remote["review_datetime"] = (first - timedelta(days=1)).isoformat()
            remote["final_rating"] = "fail"
            fake.events.append(remote)

            response = sync_progress(self.request(collection, database), fake)
            self.assertEqual(response["downloaded"], 1)
            with sqlite3.connect(database) as connection:
                rows = connection.execute(
                    "SELECT final_rating FROM reviews ORDER BY review_datetime, event_id"
                ).fetchall()
                card_json = connection.execute("SELECT card_json FROM cards").fetchone()[0]
            self.assertEqual(rows, [("fail",), ("good",)])
            self.assertIn("stability", json.loads(card_json))

    def test_legacy_local_and_populated_remote_report_bootstrap_conflict(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            self.rating(collection, database)
            with sqlite3.connect(database) as connection:
                connection.execute(
                    "UPDATE schema_metadata SET value='1' WHERE key='legacy_events_migrated'"
                )
                connection.execute(
                    "UPDATE schema_metadata SET value='[\"test.cpp.collection\"]' "
                    "WHERE key='legacy_collection_keys'"
                )
            event = {
                "event_id": "00000000-0000-4000-8000-000000000002",
                "collection_id": "test.cpp.collection",
                "exercise_id": "example",
                "review_datetime": datetime(2025, 1, 1, tzinfo=timezone.utc).isoformat(),
                "final_rating": "good", "compiled": True, "proposed_rating": "good",
                "review_status": "available", "reviewer_name": None,
                "reviewer_model": None, "reviewer_reasoning_effort": None,
                "review_attempts": 0, "solve_duration_ms": None,
                "feedback_duration_ms": None,
            }
            response = sync_progress(self.request(collection, database), FakeSupabase([event]))
            self.assertEqual(response["status"], "bootstrap_conflict")
            with sqlite3.connect(database) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM reviews").fetchone()[0], 1)

    def test_interrupted_canonical_seed_resumes_when_remote_is_local_subset(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"PRACTICE_SUPABASE_KEY": "secret-key"}
        ):
            root = Path(temporary)
            collection = self.make_collection(root)
            database = root / "practice.sqlite3"
            first = datetime(2026, 1, 1, tzinfo=timezone.utc)
            self.rating(collection, database, first)
            fake = FakeSupabase()
            sync_progress(self.request(collection, database), fake)
            self.rating(collection, database, first + timedelta(days=1), "excellent")
            with sqlite3.connect(database) as connection:
                connection.execute(
                    "UPDATE reviews SET remote_confirmed=0"
                )
                connection.execute(
                    "UPDATE sync_metadata SET bootstrap_state='uninitialized'"
                )
                connection.execute(
                    "UPDATE schema_metadata SET value='[\"test.cpp.collection\"]' "
                    "WHERE key='legacy_collection_keys'"
                )
            response = sync_progress(self.request(collection, database), fake)
            self.assertEqual(response["status"], "success")
            self.assertEqual(response["uploaded"], 1)
            self.assertEqual(len(fake.events), 2)

    def test_first_stable_access_adopts_path_keyed_history(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection = root / "collection"
            collection.mkdir()
            (collection / "example.cpp").write_text("int solve() { return 1; }\n")
            (collection / "example.md").write_text("# Example\n")
            database = root / "practice.sqlite3"
            self.rating(collection, database)
            (collection / "collection.json").write_text(
                '{"schema_version":1,"id":"test.cpp.collection"}'
            )
            store = PracticeStore(database)
            store.adopt_collection_key(str(collection.resolve()), "test.cpp.collection")
            with sqlite3.connect(database) as connection:
                keys = connection.execute("SELECT collection_key FROM reviews").fetchall()
            self.assertEqual(keys, [("test.cpp.collection",)])


if __name__ == "__main__":
    unittest.main()
