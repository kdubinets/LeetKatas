"""Persistence and collection helpers for Level C problem-solving practice."""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from practice_scheduler import (
    Card,
    SchedulerError,
    collection_keys,
    create_scheduler,
    deserialize_card,
    ensure_utc,
    rating_for,
)
from validate_level_c_collection import CollectionValidationError, validate_collection


PROBLEM_SOLVING_SCHEMA_VERSION = 3


def problem_solving_database_path(request: dict[str, Any]) -> Path:
    value = request.get("database_path")
    if value is None:
        value = os.environ.get("PROBLEM_SOLVING_DATABASE")
    if value is None:
        value = os.environ.get("PRACTICE_DATABASE")
    if value is not None and (not isinstance(value, str) or not value):
        raise SchedulerError("database_path must be a non-empty string when provided")
    if value:
        return Path(value).expanduser().resolve()
    data_home = os.environ.get("XDG_DATA_HOME")
    base = Path(data_home).expanduser() if data_home else Path.home() / ".local" / "share"
    return (base / "leetkatas" / "practice.sqlite3").resolve()


def problem_collection(value: Any) -> tuple[Path, str, list[str]]:
    path_key, collection_key, _ = collection_keys(value)
    collection = Path(path_key)
    try:
        validated = validate_collection(collection)
    except CollectionValidationError as error:
        raise SchedulerError(str(error)) from error
    return collection, collection_key, validated["problem_ids"]


class ProblemSolvingStore:
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
        connection.execute("BEGIN IMMEDIATE")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS problem_solving_cards (
                collection_key TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                card_json TEXT NOT NULL,
                due_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (collection_key, problem_id)
            );
            CREATE TABLE IF NOT EXISTS problem_solving_reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                collection_key TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                review_datetime TEXT NOT NULL,
                final_rating TEXT NOT NULL CHECK (
                    final_rating IN ('fail', 'acceptable', 'good', 'excellent')
                ),
                review_log_json TEXT NOT NULL,
                hint_used INTEGER NOT NULL CHECK (hint_used IN (0, 1)),
                clarification_used INTEGER NOT NULL CHECK (clarification_used IN (0, 1)),
                selected_at TEXT,
                revealed_at TEXT,
                solve_duration_ms INTEGER NOT NULL CHECK (solve_duration_ms >= 0),
                discussion_duration_ms INTEGER NOT NULL CHECK (discussion_duration_ms >= 0),
                remote_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (remote_confirmed IN (0, 1)),
                FOREIGN KEY (collection_key, problem_id)
                    REFERENCES problem_solving_cards (collection_key, problem_id)
            );
            CREATE INDEX IF NOT EXISTS problem_solving_reviews_collection_time_idx
                ON problem_solving_reviews(collection_key, review_datetime, event_id);
            CREATE TABLE IF NOT EXISTS problem_solving_bookmarks (
                collection_key TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                revision INTEGER NOT NULL CHECK (revision > 0),
                bookmarked_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                removed_at TEXT,
                PRIMARY KEY (collection_key, problem_id)
            );
            CREATE TABLE IF NOT EXISTS problem_solving_bookmark_events (
                event_id TEXT PRIMARY KEY,
                collection_key TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                revision INTEGER NOT NULL CHECK (revision > 0),
                action TEXT NOT NULL CHECK (action IN ('create', 'update', 'remove')),
                event_datetime TEXT NOT NULL,
                remote_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (remote_confirmed IN (0, 1))
            );
            CREATE INDEX IF NOT EXISTS problem_solving_bookmark_events_collection_idx
                ON problem_solving_bookmark_events(collection_key, event_datetime, event_id);
            CREATE TABLE IF NOT EXISTS problem_solving_artifacts (
                collection_key TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                event_id TEXT NOT NULL UNIQUE,
                revision INTEGER NOT NULL CHECK (revision > 0),
                hint_requested INTEGER NOT NULL CHECK (hint_requested IN (0, 1)),
                clarification_used INTEGER NOT NULL CHECK (clarification_used IN (0, 1)),
                revealed INTEGER NOT NULL CHECK (revealed IN (0, 1)),
                selected_at TEXT NOT NULL,
                revealed_at TEXT,
                note TEXT,
                conversation_json TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                remote_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (remote_confirmed IN (0, 1)),
                PRIMARY KEY (collection_key, problem_id)
            );
            CREATE TABLE IF NOT EXISTS problem_solving_sync_metadata (
                collection_id TEXT PRIMARY KEY,
                last_attempt_at TEXT,
                last_success_at TEXT,
                last_error TEXT,
                review_cursor INTEGER NOT NULL DEFAULT 0 CHECK (review_cursor >= 0),
                bookmark_cursor INTEGER NOT NULL DEFAULT 0 CHECK (bookmark_cursor >= 0),
                artifact_cursor INTEGER NOT NULL DEFAULT 0 CHECK (artifact_cursor >= 0)
            );
            """
        )
        review_columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(problem_solving_reviews)")
        }
        if "selected_at" not in review_columns:
            connection.execute(
                "ALTER TABLE problem_solving_reviews ADD COLUMN selected_at TEXT"
            )
        if "revealed_at" not in review_columns:
            connection.execute(
                "ALTER TABLE problem_solving_reviews ADD COLUMN revealed_at TEXT"
            )
        for table in ("problem_solving_reviews", "problem_solving_artifacts"):
            columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
            if "gave_up" in columns:
                connection.execute(f"ALTER TABLE {table} DROP COLUMN gave_up")
        artifact_columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(problem_solving_artifacts)")
        }
        if "selected_at" not in artifact_columns:
            connection.execute(
                "ALTER TABLE problem_solving_artifacts ADD COLUMN selected_at TEXT"
            )
            connection.execute(
                "UPDATE problem_solving_artifacts SET selected_at=updated_at "
                "WHERE selected_at IS NULL"
            )
        if "revealed_at" not in artifact_columns:
            connection.execute(
                "ALTER TABLE problem_solving_artifacts ADD COLUMN revealed_at TEXT"
            )
        row = connection.execute(
            "SELECT value FROM schema_metadata WHERE key='problem_solving_schema_version'"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO schema_metadata(key, value) VALUES (?, ?)",
                ("problem_solving_schema_version", str(PROBLEM_SOLVING_SCHEMA_VERSION)),
            )
        elif row["value"] in {"1", "2"}:
            connection.execute(
                "UPDATE schema_metadata SET value=? "
                "WHERE key='problem_solving_schema_version'",
                (str(PROBLEM_SOLVING_SCHEMA_VERSION),),
            )
        elif row["value"] != str(PROBLEM_SOLVING_SCHEMA_VERSION):
            connection.rollback()
            raise SchedulerError(
                f"unsupported problem-solving database schema version: {row['value']}"
            )
        connection.commit()

    def cards_for_collection(self, collection_key: str) -> dict[str, Any]:
        connection = self.connect()
        try:
            rows = connection.execute(
                "SELECT problem_id, card_json FROM problem_solving_cards WHERE collection_key=?",
                (collection_key,),
            ).fetchall()
        finally:
            connection.close()
        return {row["problem_id"]: deserialize_card(row["card_json"]) for row in rows}

    def open_bookmark_ids(self, collection_key: str) -> set[str]:
        connection = self.connect()
        try:
            rows = connection.execute(
                "SELECT problem_id FROM problem_solving_bookmarks "
                "WHERE collection_key=? AND removed_at IS NULL",
                (collection_key,),
            ).fetchall()
        finally:
            connection.close()
        return {row["problem_id"] for row in rows}

    def artifact(self, collection_key: str, problem_id: str) -> dict[str, Any] | None:
        connection = self.connect()
        try:
            row = connection.execute(
                "SELECT * FROM problem_solving_artifacts "
                "WHERE collection_key=? AND problem_id=?",
                (collection_key, problem_id),
            ).fetchone()
        finally:
            connection.close()
        if row is None:
            return None
        return {
            "revision": row["revision"],
            "hint_requested": bool(row["hint_requested"]),
            "clarification_used": bool(row["clarification_used"]),
            "revealed": bool(row["revealed"]),
            "selected_at": row["selected_at"],
            "revealed_at": row["revealed_at"],
            "note": row["note"],
            "conversation_history": json.loads(row["conversation_json"]),
            "updated_at": row["updated_at"],
        }

    def update_artifact(
        self,
        collection_key: str,
        problem_id: str,
        *,
        hint_requested: bool | None = None,
        clarification_used: bool | None = None,
        revealed: bool | None = None,
        note: str | None | object = ...,
        conversation_history: list[dict[str, str]] | None = None,
        updated_at: datetime | None = None,
    ) -> dict[str, Any]:
        current = ensure_utc(updated_at)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM problem_solving_artifacts "
                "WHERE collection_key=? AND problem_id=?",
                (collection_key, problem_id),
            ).fetchone()
            previous = dict(row) if row else {
                "revision": 0,
                "hint_requested": 0,
                "clarification_used": 0,
                "revealed": 0,
                "selected_at": current.isoformat(),
                "revealed_at": None,
                "note": None,
                "conversation_json": "[]",
            }
            revision = previous["revision"] + 1
            values = {
                "hint_requested": previous["hint_requested"] if hint_requested is None else int(hint_requested),
                "clarification_used": previous["clarification_used"] if clarification_used is None else int(clarification_used),
                "revealed": previous["revealed"] if revealed is None else int(revealed),
                "selected_at": previous["selected_at"],
                "revealed_at": (
                    previous["revealed_at"]
                    or (current.isoformat() if revealed is True else None)
                ),
                "note": previous["note"] if note is ... else note,
                "conversation_json": previous["conversation_json"] if conversation_history is None else json.dumps(conversation_history, ensure_ascii=False, separators=(",", ":")),
            }
            connection.execute(
                """INSERT INTO problem_solving_artifacts
                   (collection_key, problem_id, event_id, revision, hint_requested,
                    clarification_used, revealed, selected_at, revealed_at,
                    note, conversation_json,
                    updated_at, remote_confirmed)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                   ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                     event_id=excluded.event_id, revision=excluded.revision,
                     hint_requested=excluded.hint_requested,
                     clarification_used=excluded.clarification_used,
                     revealed=excluded.revealed,
                     selected_at=excluded.selected_at,
                     revealed_at=excluded.revealed_at,
                     note=excluded.note, conversation_json=excluded.conversation_json,
                     updated_at=excluded.updated_at, remote_confirmed=0""",
                (
                    collection_key, problem_id, str(uuid.uuid4()), revision,
                    values["hint_requested"], values["clarification_used"],
                    values["revealed"], values["selected_at"],
                    values["revealed_at"], values["note"],
                    values["conversation_json"], current.isoformat(),
                ),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return self.artifact(collection_key, problem_id) or {}

    def update_bookmark(
        self,
        collection_key: str,
        problem_id: str,
        action: str,
        note: str | None | object = ...,
        event_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = ensure_utc(event_datetime)
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM problem_solving_bookmarks "
                "WHERE collection_key=? AND problem_id=?",
                (collection_key, problem_id),
            ).fetchone()
            active = row is not None and row["removed_at"] is None
            if action == "create" and active:
                action = "update"
            if action == "update" and not active:
                raise SchedulerError("cannot update a problem that is not bookmarked")
            if action == "remove" and not active:
                raise SchedulerError("cannot remove a problem that is not bookmarked")
            revision = (row["revision"] if row else 0) + 1
            bookmarked_at = row["bookmarked_at"] if row and active else current.isoformat()
            removed_at = current.isoformat() if action == "remove" else None
            connection.execute(
                """INSERT INTO problem_solving_bookmarks
                   (collection_key, problem_id, revision, bookmarked_at, updated_at, removed_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                     revision=excluded.revision, bookmarked_at=excluded.bookmarked_at,
                     updated_at=excluded.updated_at, removed_at=excluded.removed_at""",
                (
                    collection_key, problem_id, revision, bookmarked_at,
                    current.isoformat(), removed_at,
                ),
            )
            event_id = str(uuid.uuid4())
            connection.execute(
                """INSERT INTO problem_solving_bookmark_events
                   (event_id, collection_key, problem_id, revision, action, event_datetime)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (event_id, collection_key, problem_id, revision, action, current.isoformat()),
            )
            if action != "remove" and note is not ...:
                artifact = connection.execute(
                    "SELECT * FROM problem_solving_artifacts "
                    "WHERE collection_key=? AND problem_id=?",
                    (collection_key, problem_id),
                ).fetchone()
                artifact_revision = (artifact["revision"] if artifact else 0) + 1
                connection.execute(
                    """INSERT INTO problem_solving_artifacts
                       (collection_key, problem_id, event_id, revision,
                        hint_requested, clarification_used, revealed,
                        selected_at, revealed_at, note, conversation_json,
                        updated_at, remote_confirmed)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                       ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                         event_id=excluded.event_id, revision=excluded.revision,
                         hint_requested=excluded.hint_requested,
                         clarification_used=excluded.clarification_used,
                         revealed=excluded.revealed,
                         selected_at=excluded.selected_at,
                         revealed_at=excluded.revealed_at,
                         note=excluded.note,
                         conversation_json=excluded.conversation_json,
                         updated_at=excluded.updated_at, remote_confirmed=0""",
                    (
                        collection_key, problem_id, str(uuid.uuid4()), artifact_revision,
                        artifact["hint_requested"] if artifact else 0,
                        artifact["clarification_used"] if artifact else 0,
                        artifact["revealed"] if artifact else 0,
                        artifact["selected_at"] if artifact else current.isoformat(),
                        artifact["revealed_at"] if artifact else None,
                        note, artifact["conversation_json"] if artifact else "[]",
                        current.isoformat(),
                    ),
                )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        result = {
            "problem_id": problem_id,
            "bookmarked": action != "remove",
            "action": action,
            "revision": revision,
            "updated_at": current.isoformat(),
        }
        if action != "remove" and note is not ...:
            result["state"] = self.artifact(collection_key, problem_id)
        return result

    def list_bookmarks(self, collection_key: str) -> list[dict[str, Any]]:
        connection = self.connect()
        try:
            rows = connection.execute(
                """SELECT b.*, a.note, a.hint_requested, a.revealed
                   FROM problem_solving_bookmarks b
                   LEFT JOIN problem_solving_artifacts a
                     ON a.collection_key=b.collection_key AND a.problem_id=b.problem_id
                   WHERE b.collection_key=? AND b.removed_at IS NULL
                   ORDER BY b.updated_at, b.problem_id""",
                (collection_key,),
            ).fetchall()
        finally:
            connection.close()
        return [
            {
                "problem_id": row["problem_id"],
                "revision": row["revision"],
                "bookmarked_at": row["bookmarked_at"],
                "updated_at": row["updated_at"],
                "note": row["note"],
                "hint_requested": bool(row["hint_requested"]) if row["hint_requested"] is not None else False,
                "revealed": bool(row["revealed"]) if row["revealed"] is not None else False,
            }
            for row in rows
        ]

    def record_review(
        self,
        collection_key: str,
        problem_id: str,
        final_rating: str,
        solve_duration_ms: int,
        discussion_duration_ms: int,
        review_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = ensure_utc(review_datetime)
        scheduler = create_scheduler()
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            artifact = connection.execute(
                "SELECT * FROM problem_solving_artifacts "
                "WHERE collection_key=? AND problem_id=?",
                (collection_key, problem_id),
            ).fetchone()
            if artifact is None or not artifact["revealed"]:
                raise SchedulerError("rating is permitted only after the solution outline is revealed")
            row = connection.execute(
                "SELECT card_json FROM problem_solving_cards "
                "WHERE collection_key=? AND problem_id=?",
                (collection_key, problem_id),
            ).fetchone()
            card = Card(due=current) if row is None else deserialize_card(row["card_json"])
            updated_card, review_log = scheduler.review_card(
                card, rating_for(final_rating), review_datetime=current
            )
            timestamp = current.isoformat()
            connection.execute(
                """INSERT INTO problem_solving_cards
                   (collection_key, problem_id, card_json, due_at, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                     card_json=excluded.card_json, due_at=excluded.due_at,
                     updated_at=excluded.updated_at""",
                (
                    collection_key, problem_id, updated_card.to_json(),
                    updated_card.due.isoformat(), timestamp, timestamp,
                ),
            )
            event_id = str(uuid.uuid4())
            connection.execute(
                """INSERT INTO problem_solving_reviews
                   (event_id, collection_key, problem_id, review_datetime,
                    final_rating, review_log_json, hint_used, clarification_used,
                    selected_at, revealed_at, solve_duration_ms,
                    discussion_duration_ms)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    event_id, collection_key, problem_id,
                    review_log.review_datetime.isoformat(), final_rating,
                    review_log.to_json(), artifact["hint_requested"],
                    artifact["clarification_used"], artifact["selected_at"], artifact["revealed_at"],
                    solve_duration_ms, discussion_duration_ms,
                ),
            )
            bookmarked = connection.execute(
                "SELECT 1 FROM problem_solving_bookmarks "
                "WHERE collection_key=? AND problem_id=? AND removed_at IS NULL",
                (collection_key, problem_id),
            ).fetchone() is not None
            if not bookmarked:
                connection.execute(
                    "DELETE FROM problem_solving_artifacts "
                    "WHERE collection_key=? AND problem_id=?",
                    (collection_key, problem_id),
                )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {
            "recorded": True,
            "event_id": event_id,
            "due": updated_card.due.isoformat(),
            "state": updated_card.state.name.lower(),
            "bookmark_retained": bookmarked,
        }


def replay_problem_cards(
    connection: sqlite3.Connection, collection_key: str, problem_ids: set[str]
) -> None:
    """Rebuild FSRS cards deterministically after synchronized review imports."""
    scheduler = create_scheduler()
    for problem_id in problem_ids:
        rows = connection.execute(
            """SELECT review_id, review_datetime, final_rating
               FROM problem_solving_reviews
               WHERE collection_key=? AND problem_id=?
               ORDER BY review_datetime, event_id""",
            (collection_key, problem_id),
        ).fetchall()
        if not rows:
            continue
        card = None
        for row in rows:
            reviewed_at = datetime.fromisoformat(row["review_datetime"])
            if card is None:
                card = Card(due=reviewed_at)
            card, review_log = scheduler.review_card(
                card, rating_for(row["final_rating"]), review_datetime=reviewed_at
            )
            connection.execute(
                "UPDATE problem_solving_reviews SET review_log_json=? WHERE review_id=?",
                (review_log.to_json(), row["review_id"]),
            )
        connection.execute(
            """INSERT INTO problem_solving_cards
               (collection_key, problem_id, card_json, due_at, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                 card_json=excluded.card_json, due_at=excluded.due_at,
                 updated_at=excluded.updated_at""",
            (
                collection_key, problem_id, card.to_json(), card.due.isoformat(),
                rows[0]["review_datetime"], rows[-1]["review_datetime"],
            ),
        )
