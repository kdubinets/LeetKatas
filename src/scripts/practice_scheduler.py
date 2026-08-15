"""Persistent FSRS scheduling and review history for practice exercises."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from fsrs import Card, Rating, Scheduler
except ImportError as error:  # Reported through the scripts' JSON protocol.
    Card = Rating = Scheduler = None  # type: ignore[assignment,misc]
    FSRS_IMPORT_ERROR: ImportError | None = error
else:
    FSRS_IMPORT_ERROR = None


SCHEMA_VERSION = 7
RATING_NAMES = {"fail", "acceptable", "good", "excellent"}
COLLECTION_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)+$")


class SchedulerError(ValueError):
    """Raised when scheduler configuration or persistent state is invalid."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def require_fsrs() -> None:
    if FSRS_IMPORT_ERROR is not None:
        raise SchedulerError(
            "FSRS dependency is unavailable; install fsrs==6.3.1 for PRACTICE_PYTHON"
        ) from FSRS_IMPORT_ERROR


def canonical_collection(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise SchedulerError("exercise_directory must be a non-empty string")
    collection = Path(value).expanduser()
    if not collection.is_dir():
        raise SchedulerError(f"exercise directory does not exist: {collection}")
    return str(collection.resolve())


def collection_identity(collection: str | Path) -> str | None:
    """Return a collection's portable identity, or None for local-only collections."""
    metadata = Path(collection) / "collection.json"
    if not metadata.is_file():
        return None
    try:
        document = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if (
        not isinstance(document, dict)
        or type(document.get("schema_version")) is not int
        or document["schema_version"] != 1
    ):
        return None
    identity = document.get("id")
    if not isinstance(identity, str) or not COLLECTION_ID_PATTERN.fullmatch(identity):
        return None
    return identity


def collection_keys(value: Any) -> tuple[str, str, str | None]:
    """Return absolute path, scheduler key, and optional synchronization identity."""
    path_key = canonical_collection(value)
    identity = collection_identity(path_key)
    return path_key, identity or path_key, identity


def database_path(request: dict[str, Any]) -> Path:
    value = request.get("database_path")
    if value is None:
        value = os.environ.get("PRACTICE_DATABASE")
    if value is not None and (not isinstance(value, str) or not value):
        raise SchedulerError("database_path must be a non-empty string when provided")
    if value:
        return Path(value).expanduser().resolve()

    data_home = os.environ.get("XDG_DATA_HOME")
    base = Path(data_home).expanduser() if data_home else Path.home() / ".local" / "share"
    return (base / "leetkatas" / "practice.sqlite3").resolve()


def ensure_utc(value: datetime | None) -> datetime:
    current = value or utc_now()
    if current.tzinfo != timezone.utc:
        raise SchedulerError("scheduler datetime must be timezone-aware and set to UTC")
    return current


def create_scheduler() -> Any:
    require_fsrs()
    return Scheduler(desired_retention=0.9, enable_fuzzing=True)


def deserialize_card(serialized: str) -> Any:
    require_fsrs()
    try:
        return Card.from_json(serialized)
    except (KeyError, TypeError, ValueError) as error:
        raise SchedulerError("stored FSRS card is invalid") from error


def rating_for(name: str) -> Any:
    require_fsrs()
    ratings = {
        "fail": Rating.Again,
        "acceptable": Rating.Hard,
        "good": Rating.Good,
        "excellent": Rating.Easy,
    }
    try:
        return ratings[name]
    except KeyError as error:
        raise SchedulerError("final_rating must be a valid rating") from error


class PracticeStore:
    """Small SQLite repository shared by selector and recorder processes."""

    def __init__(self, path: Path):
        self.path = path

    def connect(self) -> sqlite3.Connection:
        connection: sqlite3.Connection | None = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(self.path, timeout=5)
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            self._ensure_schema(connection)
            return connection
        except (OSError, sqlite3.Error) as error:
            if connection is not None:
                connection.close()
            raise SchedulerError(
                f"could not open practice database {self.path}: {error}"
            ) from error
        except SchedulerError:
            if connection is not None:
                connection.close()
            raise

    def _ensure_schema(self, connection: sqlite3.Connection) -> None:
        had_reviews_table = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='reviews'"
        ).fetchone() is not None
        preexisting_reviews = (
            connection.execute("SELECT count(*) FROM reviews").fetchone()[0]
            if had_reviews_table else 0
        )
        preexisting_collection_keys = (
            [row[0] for row in connection.execute(
                "SELECT DISTINCT collection_key FROM reviews ORDER BY collection_key"
            )]
            if preexisting_reviews else []
        )
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS cards (
                collection_key TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                card_json TEXT NOT NULL,
                due_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (collection_key, exercise_id)
            );
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                collection_key TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                review_datetime TEXT NOT NULL,
                final_rating TEXT NOT NULL,
                compiled INTEGER NOT NULL CHECK (compiled IN (0, 1)),
                proposed_rating TEXT,
                review_status TEXT NOT NULL DEFAULT 'legacy',
                reviewer_name TEXT,
                reviewer_model TEXT,
                reviewer_reasoning_effort TEXT,
                reviewer_service_tier TEXT,
                reviewer_usage_json TEXT,
                review_attempts INTEGER NOT NULL DEFAULT 0,
                solve_duration_ms INTEGER CHECK (solve_duration_ms >= 0),
                feedback_duration_ms INTEGER CHECK (feedback_duration_ms >= 0),
                review_log_json TEXT NOT NULL,
                remote_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (remote_confirmed IN (0, 1)),
                FOREIGN KEY (collection_key, exercise_id)
                    REFERENCES cards (collection_key, exercise_id)
            );
            """
        )
        # Startup can launch selection and best-effort synchronization together.
        # Serialize the remainder of a schema upgrade so both processes do not
        # inspect an old table shape and then attempt the same ALTER TABLE.
        connection.execute("BEGIN IMMEDIATE")
        columns = {row[1] for row in connection.execute("PRAGMA table_info(reviews)")}
        proposed_info = next((row for row in connection.execute("PRAGMA table_info(reviews)") if row[1] == "proposed_rating"), None)
        if proposed_info is not None and proposed_info[3]:
            connection.execute("ALTER TABLE reviews RENAME TO reviews_legacy_v1")
            connection.execute("""CREATE TABLE reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT, collection_key TEXT NOT NULL,
                exercise_id TEXT NOT NULL, review_datetime TEXT NOT NULL, final_rating TEXT NOT NULL,
                compiled INTEGER NOT NULL CHECK (compiled IN (0, 1)), proposed_rating TEXT,
                review_log_json TEXT NOT NULL, review_status TEXT NOT NULL DEFAULT 'legacy',
                reviewer_name TEXT, reviewer_model TEXT, reviewer_reasoning_effort TEXT,
                review_attempts INTEGER NOT NULL DEFAULT 0,
                solve_duration_ms INTEGER CHECK (solve_duration_ms >= 0),
                feedback_duration_ms INTEGER CHECK (feedback_duration_ms >= 0),
                FOREIGN KEY (collection_key, exercise_id) REFERENCES cards (collection_key, exercise_id))""")
            connection.execute("""INSERT INTO reviews (review_id,collection_key,exercise_id,review_datetime,final_rating,compiled,proposed_rating,review_log_json)
                SELECT review_id,collection_key,exercise_id,review_datetime,final_rating,compiled,proposed_rating,review_log_json FROM reviews_legacy_v1""")
            connection.execute("DROP TABLE reviews_legacy_v1")
            columns = {"review_status", "reviewer_name", "reviewer_model", "reviewer_reasoning_effort", "review_attempts"}
        for name, definition in (("review_status", "TEXT NOT NULL DEFAULT 'legacy'"), ("reviewer_name", "TEXT"), ("reviewer_model", "TEXT"), ("reviewer_reasoning_effort", "TEXT"), ("reviewer_service_tier", "TEXT"), ("reviewer_usage_json", "TEXT"), ("review_attempts", "INTEGER NOT NULL DEFAULT 0")):
            if name not in columns:
                connection.execute(f"ALTER TABLE reviews ADD COLUMN {name} {definition}")
        columns = {row[1] for row in connection.execute("PRAGMA table_info(reviews)")}
        for name in ("solve_duration_ms", "feedback_duration_ms"):
            if name not in columns:
                connection.execute(
                    f"ALTER TABLE reviews ADD COLUMN {name} INTEGER CHECK ({name} >= 0)"
                )
        columns = {row[1] for row in connection.execute("PRAGMA table_info(reviews)")}
        if "event_id" not in columns:
            connection.execute("ALTER TABLE reviews ADD COLUMN event_id TEXT")
        if "remote_confirmed" not in columns:
            connection.execute(
                "ALTER TABLE reviews ADD COLUMN remote_confirmed INTEGER NOT NULL DEFAULT 0"
            )
        missing_event_ids = connection.execute(
            "SELECT review_id FROM reviews WHERE event_id IS NULL OR event_id = ''"
        ).fetchall()
        for missing in missing_event_ids:
            connection.execute(
                "UPDATE reviews SET event_id = ? WHERE review_id = ?",
                (str(uuid.uuid4()), missing["review_id"]),
            )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS reviews_event_id_idx ON reviews(event_id)"
        )
        connection.execute(
            """CREATE TRIGGER IF NOT EXISTS reviews_require_event_id
               BEFORE INSERT ON reviews
               WHEN NEW.event_id IS NULL OR NEW.event_id = ''
               BEGIN SELECT RAISE(ABORT, 'review event_id is required'); END"""
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS reviews_collection_time_idx "
            "ON reviews(collection_key, review_datetime, event_id)"
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS sync_metadata (
                collection_id TEXT PRIMARY KEY,
                bootstrap_state TEXT NOT NULL DEFAULT 'uninitialized',
                last_attempt_at TEXT,
                last_success_at TEXT,
                last_error TEXT,
                last_remote_sequence INTEGER CHECK (
                    last_remote_sequence IS NULL OR last_remote_sequence >= 0
                )
            )"""
        )
        sync_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(sync_metadata)")
        }
        if "last_remote_sequence" not in sync_columns:
            connection.execute(
                "ALTER TABLE sync_metadata ADD COLUMN last_remote_sequence INTEGER "
                "CHECK (last_remote_sequence IS NULL OR last_remote_sequence >= 0)"
            )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS review_artifacts (
                review_id INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                submitted_source TEXT NOT NULL,
                review_response_json TEXT NOT NULL,
                FOREIGN KEY (review_id) REFERENCES reviews (review_id)
                    ON DELETE CASCADE
            )"""
        )
        row = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO schema_metadata (key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
        elif row["value"] in {"1", "2", "3", "4", "5", "6"}:
            connection.execute("UPDATE schema_metadata SET value = ? WHERE key = 'schema_version'", (str(SCHEMA_VERSION),))
        elif row["value"] != str(SCHEMA_VERSION):
            raise SchedulerError(
                f"unsupported practice database schema version: {row['value']}"
            )
        legacy_marker = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'legacy_events_migrated'"
        ).fetchone()
        if legacy_marker is None:
            connection.execute(
                "INSERT INTO schema_metadata (key, value) VALUES ('legacy_events_migrated', ?)",
                ("1" if had_reviews_table and preexisting_reviews else "0",),
            )
            connection.execute(
                "INSERT INTO schema_metadata (key, value) VALUES ('legacy_collection_keys', ?)",
                (json.dumps(preexisting_collection_keys, separators=(",", ":")),),
            )
        elif connection.execute(
            "SELECT 1 FROM schema_metadata WHERE key='legacy_collection_keys'"
        ).fetchone() is None:
            connection.execute(
                "INSERT INTO schema_metadata (key, value) VALUES ('legacy_collection_keys', '[]')"
            )
        connection.commit()

    def adopt_collection_key(self, path_key: str, collection_key: str) -> None:
        """Transactionally adopt legacy absolute-path state into a stable identity."""
        if path_key == collection_key:
            return
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """INSERT OR IGNORE INTO cards
                   (collection_key, exercise_id, card_json, due_at, created_at, updated_at)
                   SELECT ?, exercise_id, card_json, due_at, created_at, updated_at
                   FROM cards WHERE collection_key = ?""",
                (collection_key, path_key),
            )
            connection.execute(
                "UPDATE reviews SET collection_key = ? WHERE collection_key = ?",
                (collection_key, path_key),
            )
            connection.execute("DELETE FROM cards WHERE collection_key = ?", (path_key,))
            legacy_row = connection.execute(
                "SELECT value FROM schema_metadata WHERE key='legacy_collection_keys'"
            ).fetchone()
            if legacy_row is not None:
                try:
                    legacy_keys = json.loads(legacy_row["value"])
                except json.JSONDecodeError:
                    legacy_keys = []
                if path_key in legacy_keys and collection_key not in legacy_keys:
                    legacy_keys = [collection_key if key == path_key else key for key in legacy_keys]
                    connection.execute(
                        "UPDATE schema_metadata SET value=? WHERE key='legacy_collection_keys'",
                        (json.dumps(legacy_keys, separators=(",", ":")),),
                    )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def cards_for_collection(self, collection_key: str) -> dict[str, Any]:
        require_fsrs()
        connection = self.connect()
        try:
            rows = connection.execute(
                "SELECT exercise_id, card_json FROM cards WHERE collection_key = ?",
                (collection_key,),
            ).fetchall()
        finally:
            connection.close()
        return {row["exercise_id"]: deserialize_card(row["card_json"]) for row in rows}

    def record_review(
        self,
        collection_key: str,
        exercise_id: str,
        compiled: bool,
        proposed_rating: str | None,
        final_rating: str,
        review_datetime: datetime | None = None,
        review_status: str = "available",
        reviewer_name: str | None = None,
        reviewer_model: str | None = None,
        reviewer_reasoning_effort: str | None = None,
        reviewer_service_tier: str | None = None,
        reviewer_usage: dict[str, Any] | None = None,
        review_attempts: int = 0,
        solve_duration_ms: int | None = None,
        feedback_duration_ms: int | None = None,
        submitted_source: str | None = None,
        review_response: dict[str, Any] | None = None,
        review_archive_ttl_days: int = 30,
    ) -> dict[str, str | bool]:
        current = ensure_utc(review_datetime)
        scheduler = create_scheduler()
        connection = self.connect()
        archive_enabled = (
            review_archive_ttl_days > 0
            and submitted_source is not None
            and review_response is not None
        )
        if archive_enabled:
            self.path.chmod(0o600)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "DELETE FROM review_artifacts WHERE expires_at <= ?", (current.isoformat(),)
            )
            row = connection.execute(
                """
                SELECT card_json FROM cards
                WHERE collection_key = ? AND exercise_id = ?
                """,
                (collection_key, exercise_id),
            ).fetchone()
            if row is None:
                card = Card(due=current)
            else:
                card = deserialize_card(row["card_json"])

            updated_card, review_log = scheduler.review_card(
                card, rating_for(final_rating), review_datetime=current
            )
            timestamp = current.isoformat()
            connection.execute(
                """
                INSERT INTO cards (
                    collection_key, exercise_id, card_json, due_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (collection_key, exercise_id) DO UPDATE SET
                    card_json = excluded.card_json,
                    due_at = excluded.due_at,
                    updated_at = excluded.updated_at
                """,
                (
                    collection_key,
                    exercise_id,
                    updated_card.to_json(),
                    updated_card.due.isoformat(),
                    timestamp,
                    timestamp,
                ),
            )
            review_cursor = connection.execute(
                """
                INSERT INTO reviews (
                    event_id, collection_key, exercise_id, review_datetime, final_rating,
                    compiled, proposed_rating, review_log_json, review_status,
                    reviewer_name, reviewer_model, reviewer_reasoning_effort, reviewer_service_tier, reviewer_usage_json,
                    review_attempts, solve_duration_ms, feedback_duration_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    collection_key,
                    exercise_id,
                    review_log.review_datetime.isoformat(),
                    final_rating,
                    int(compiled),
                    proposed_rating,
                    review_log.to_json(),
                    review_status,
                    reviewer_name,
                    reviewer_model,
                    reviewer_reasoning_effort,
                    reviewer_service_tier,
                    json.dumps(reviewer_usage, separators=(",", ":")) if reviewer_usage else None,
                    review_attempts,
                    solve_duration_ms,
                    feedback_duration_ms,
                ),
            )
            if archive_enabled:
                expires_at = current + timedelta(days=review_archive_ttl_days)
                connection.execute(
                    """
                    INSERT INTO review_artifacts (
                        review_id, created_at, expires_at, submitted_source,
                        review_response_json
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        review_cursor.lastrowid,
                        current.isoformat(),
                        expires_at.isoformat(),
                        submitted_source,
                        json.dumps(review_response, ensure_ascii=False, separators=(",", ":")),
                    ),
                )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return {
            "recorded": True,
            "due": updated_card.due.isoformat(),
            "state": updated_card.state.name.lower(),
        }
