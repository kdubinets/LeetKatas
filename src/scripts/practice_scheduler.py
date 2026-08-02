"""Persistent FSRS scheduling and review history for practice exercises."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from fsrs import Card, Rating, Scheduler
except ImportError as error:  # Reported through the scripts' JSON protocol.
    Card = Rating = Scheduler = None  # type: ignore[assignment,misc]
    FSRS_IMPORT_ERROR: ImportError | None = error
else:
    FSRS_IMPORT_ERROR = None


SCHEMA_VERSION = 2
RATING_NAMES = {"fail", "acceptable", "good", "excellent"}


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
                collection_key TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                review_datetime TEXT NOT NULL,
                final_rating TEXT NOT NULL,
                compiled INTEGER NOT NULL CHECK (compiled IN (0, 1)),
                proposed_rating TEXT,
                review_status TEXT NOT NULL DEFAULT 'legacy',
                reviewer_name TEXT,
                reviewer_model TEXT,
                review_attempts INTEGER NOT NULL DEFAULT 0,
                review_log_json TEXT NOT NULL,
                FOREIGN KEY (collection_key, exercise_id)
                    REFERENCES cards (collection_key, exercise_id)
            );
            """
        )
        columns = {row[1] for row in connection.execute("PRAGMA table_info(reviews)")}
        proposed_info = next((row for row in connection.execute("PRAGMA table_info(reviews)") if row[1] == "proposed_rating"), None)
        if proposed_info is not None and proposed_info[3]:
            connection.execute("ALTER TABLE reviews RENAME TO reviews_legacy_v1")
            connection.execute("""CREATE TABLE reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT, collection_key TEXT NOT NULL,
                exercise_id TEXT NOT NULL, review_datetime TEXT NOT NULL, final_rating TEXT NOT NULL,
                compiled INTEGER NOT NULL CHECK (compiled IN (0, 1)), proposed_rating TEXT,
                review_log_json TEXT NOT NULL, review_status TEXT NOT NULL DEFAULT 'legacy',
                reviewer_name TEXT, reviewer_model TEXT, review_attempts INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (collection_key, exercise_id) REFERENCES cards (collection_key, exercise_id))""")
            connection.execute("""INSERT INTO reviews (review_id,collection_key,exercise_id,review_datetime,final_rating,compiled,proposed_rating,review_log_json)
                SELECT review_id,collection_key,exercise_id,review_datetime,final_rating,compiled,proposed_rating,review_log_json FROM reviews_legacy_v1""")
            connection.execute("DROP TABLE reviews_legacy_v1")
            columns = {"review_status", "reviewer_name", "reviewer_model", "review_attempts"}
        for name, definition in (("review_status", "TEXT NOT NULL DEFAULT 'legacy'"), ("reviewer_name", "TEXT"), ("reviewer_model", "TEXT"), ("review_attempts", "INTEGER NOT NULL DEFAULT 0")):
            if name not in columns:
                connection.execute(f"ALTER TABLE reviews ADD COLUMN {name} {definition}")
        row = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO schema_metadata (key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
        elif row["value"] == "1":
            connection.execute("UPDATE schema_metadata SET value = ? WHERE key = 'schema_version'", (str(SCHEMA_VERSION),))
        elif row["value"] != str(SCHEMA_VERSION):
            raise SchedulerError(
                f"unsupported practice database schema version: {row['value']}"
            )
        connection.commit()

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
        review_attempts: int = 0,
    ) -> dict[str, str | bool]:
        current = ensure_utc(review_datetime)
        scheduler = create_scheduler()
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
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
            connection.execute(
                """
                INSERT INTO reviews (
                    collection_key, exercise_id, review_datetime, final_rating,
                    compiled, proposed_rating, review_log_json, review_status,
                    reviewer_name, reviewer_model, review_attempts
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
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
                    review_attempts,
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
