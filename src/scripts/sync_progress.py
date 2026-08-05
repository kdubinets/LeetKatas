#!/usr/bin/env python3
"""Best-effort append-only synchronization of practice review events."""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from practice_scheduler import (
    PracticeStore,
    RATING_NAMES,
    SchedulerError,
    collection_keys,
    create_scheduler,
    database_path,
    rating_for,
    Card,
)


PAGE_SIZE = 200
UPLOAD_BATCH_SIZE = 100
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
REMOTE_FIELDS = (
    "sync_sequence,event_id,collection_id,exercise_id,review_datetime,final_rating,compiled,"
    "proposed_rating,review_status,reviewer_name,reviewer_model,"
    "reviewer_reasoning_effort,review_attempts,solve_duration_ms,feedback_duration_ms"
)


class SyncError(ValueError):
    pass


class UnavailableError(RuntimeError):
    pass


class HttpAdapter(Protocol):
    def request(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None
    ) -> tuple[int, bytes]: ...


class UrllibAdapter:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def request(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None
    ) -> tuple[int, bytes]:
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body_bytes = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body_bytes) > MAX_RESPONSE_BYTES:
                    raise UnavailableError("remote response is too large")
                return response.status, body_bytes
        except urllib.error.HTTPError as error:
            return error.code, b""
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise UnavailableError("network request failed") from error


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def required_text(value: Any, name: str, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value or len(value) > 512:
        raise UnavailableError(f"remote event has invalid {name}")
    return value


def validate_event(value: Any, collection_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise UnavailableError("remote response contains a non-object event")
    sync_sequence = value.get("sync_sequence")
    if type(sync_sequence) is not int or sync_sequence <= 0:
        raise UnavailableError("remote event has invalid sync_sequence")
    event_id = required_text(value.get("event_id"), "event_id")
    try:
        parsed_id = uuid.UUID(event_id)
    except (ValueError, AttributeError) as error:
        raise UnavailableError("remote event has invalid event_id") from error
    if str(parsed_id) != event_id:
        raise UnavailableError("remote event has non-canonical event_id")
    if value.get("collection_id") != collection_id:
        raise UnavailableError("remote event has an unexpected collection_id")
    exercise_id = required_text(value.get("exercise_id"), "exercise_id")
    reviewed = required_text(value.get("review_datetime"), "review_datetime")
    try:
        reviewed_at = datetime.fromisoformat(reviewed)
    except ValueError as error:
        raise UnavailableError("remote event has invalid review_datetime") from error
    if reviewed_at.tzinfo is None or reviewed_at.utcoffset() != timezone.utc.utcoffset(reviewed_at):
        raise UnavailableError("remote event review_datetime must be UTC")
    final_rating = value.get("final_rating")
    proposed_rating = value.get("proposed_rating")
    if final_rating not in RATING_NAMES:
        raise UnavailableError("remote event has invalid final_rating")
    if proposed_rating is not None and proposed_rating not in RATING_NAMES:
        raise UnavailableError("remote event has invalid proposed_rating")
    if not isinstance(value.get("compiled"), bool):
        raise UnavailableError("remote event has invalid compiled")
    attempts = value.get("review_attempts", 0)
    if type(attempts) is not int or attempts < 0:
        raise UnavailableError("remote event has invalid review_attempts")
    durations: list[int | None] = []
    for field in ("solve_duration_ms", "feedback_duration_ms"):
        duration = value.get(field)
        if duration is not None and (type(duration) is not int or duration < 0):
            raise UnavailableError(f"remote event has invalid {field}")
        durations.append(duration)
    if (durations[0] is None) != (durations[1] is None):
        raise UnavailableError("remote event has incomplete duration fields")
    return {
        "sync_sequence": sync_sequence,
        "event_id": event_id,
        "collection_id": collection_id,
        "exercise_id": exercise_id,
        "review_datetime": reviewed_at.isoformat(),
        "final_rating": final_rating,
        "compiled": value["compiled"],
        "proposed_rating": proposed_rating,
        "review_status": required_text(value.get("review_status", "legacy"), "review_status"),
        "reviewer_name": required_text(value.get("reviewer_name"), "reviewer_name", True),
        "reviewer_model": required_text(value.get("reviewer_model"), "reviewer_model", True),
        "reviewer_reasoning_effort": required_text(
            value.get("reviewer_reasoning_effort"), "reviewer_reasoning_effort", True
        ),
        "review_attempts": attempts,
        "solve_duration_ms": durations[0],
        "feedback_duration_ms": durations[1],
    }


def remote_event(row: sqlite3.Row, collection_id: str) -> dict[str, Any]:
    return {
        "event_id": row["event_id"],
        "collection_id": collection_id,
        "exercise_id": row["exercise_id"],
        "review_datetime": row["review_datetime"],
        "final_rating": row["final_rating"],
        "compiled": bool(row["compiled"]),
        "proposed_rating": row["proposed_rating"],
        "review_status": row["review_status"],
        "reviewer_name": row["reviewer_name"],
        "reviewer_model": row["reviewer_model"],
        "reviewer_reasoning_effort": row["reviewer_reasoning_effort"],
        "review_attempts": row["review_attempts"],
        "solve_duration_ms": row["solve_duration_ms"],
        "feedback_duration_ms": row["feedback_duration_ms"],
    }


def event_payload(event: dict[str, Any]) -> dict[str, Any]:
    """Return the immutable event fields shared by local and remote ledgers."""
    return {name: value for name, value in event.items() if name != "sync_sequence"}


def headers(key: str, prefer: str | None = None) -> dict[str, str]:
    result = {
        "apikey": key,
        "Content-Type": "application/json",
    }
    if prefer:
        result["Prefer"] = prefer
    return result


def check_status(status: int) -> None:
    if status in {401, 403}:
        raise UnavailableError("authentication failed")
    if status == 429:
        raise UnavailableError("remote rate limit reached")
    if status < 200 or status >= 300:
        raise UnavailableError("remote service unavailable")


def fetch_remote(
    adapter: HttpAdapter,
    base_url: str,
    key: str,
    collection_id: str,
    after_sequence: int,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    cursor = after_sequence
    encoded_collection = urllib.parse.quote(collection_id, safe="")
    while True:
        query = (
            f"collection_id=eq.{encoded_collection}&select={REMOTE_FIELDS}"
            f"&sync_sequence=gt.{cursor}&order=sync_sequence.asc&limit={PAGE_SIZE}"
        )
        status, body = adapter.request(
            "GET", f"{base_url}/rest/v1/practice_review_events?{query}", headers(key), None
        )
        if status == 400:
            raise UnavailableError(
                "remote sync schema is outdated; rerun supabase_setup.sql"
            )
        check_status(status)
        try:
            page = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise UnavailableError("remote service returned malformed JSON") from error
        if not isinstance(page, list):
            raise UnavailableError("remote service returned an invalid event page")
        validated = [validate_event(event, collection_id) for event in page]
        sequences = [event["sync_sequence"] for event in validated]
        if sequences != sorted(sequences) or any(sequence <= cursor for sequence in sequences):
            raise UnavailableError("remote response contains unordered sync sequences")
        if len(sequences) != len(set(sequences)):
            raise UnavailableError("remote response contains duplicate sync sequences")
        if any(event["event_id"] in event_ids for event in validated) or len({
            event["event_id"] for event in validated
        }) != len(validated):
            raise UnavailableError("remote response contains duplicate event UUIDs")
        events.extend(validated)
        event_ids.update(event["event_id"] for event in validated)
        if validated:
            cursor = validated[-1]["sync_sequence"]
        if len(page) < PAGE_SIZE:
            return events


def upload_events(
    adapter: HttpAdapter, base_url: str, key: str, events: list[dict[str, Any]]
) -> None:
    for start in range(0, len(events), UPLOAD_BATCH_SIZE):
        payload = json.dumps(events[start : start + UPLOAD_BATCH_SIZE], separators=(",", ":")).encode()
        status, _ = adapter.request(
            "POST",
            f"{base_url}/rest/v1/practice_review_events?on_conflict=event_id",
            headers(key, "resolution=ignore-duplicates,return=minimal"),
            payload,
        )
        check_status(status)


def replay_exercises(connection: sqlite3.Connection, collection_id: str, ids: set[str]) -> None:
    scheduler = create_scheduler()
    for exercise_id in ids:
        rows = connection.execute(
            """SELECT review_id, review_datetime, final_rating FROM reviews
               WHERE collection_key = ? AND exercise_id = ?
               ORDER BY review_datetime, event_id""",
            (collection_id, exercise_id),
        ).fetchall()
        card = None
        created_at = rows[0]["review_datetime"]
        for row in rows:
            reviewed_at = datetime.fromisoformat(row["review_datetime"])
            if card is None:
                card = Card(due=reviewed_at)
            card, review_log = scheduler.review_card(
                card, rating_for(row["final_rating"]), review_datetime=reviewed_at
            )
            connection.execute(
                "UPDATE reviews SET review_log_json = ? WHERE review_id = ?",
                (review_log.to_json(), row["review_id"]),
            )
        connection.execute(
            """INSERT INTO cards
               (collection_key, exercise_id, card_json, due_at, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(collection_key, exercise_id) DO UPDATE SET
                 card_json=excluded.card_json, due_at=excluded.due_at,
                 updated_at=excluded.updated_at""",
            (
                collection_id,
                exercise_id,
                card.to_json(),
                card.due.isoformat(),
                created_at,
                rows[-1]["review_datetime"],
            ),
        )


def sync_progress(
    request: dict[str, Any], adapter: HttpAdapter | None = None
) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise SyncError("request must be a JSON object")
    path_key, collection_key, collection_id = collection_keys(request.get("exercise_directory"))
    store = PracticeStore(database_path(request))
    store.adopt_collection_key(path_key, collection_key)
    connection = store.connect()
    try:
        if collection_id is None:
            pending = 0
            metadata = None
        else:
            pending = connection.execute(
                "SELECT count(*) FROM reviews WHERE collection_key = ? AND remote_confirmed = 0",
                (collection_id,),
            ).fetchone()[0]
            metadata = connection.execute(
                "SELECT * FROM sync_metadata WHERE collection_id = ?", (collection_id,)
            ).fetchone()
        status_response = {
            "status": "disabled",
            "configured": False,
            "pending": pending,
            "last_success": metadata["last_success_at"] if metadata else None,
        }
        action = request.get("action", "sync")
        if action not in {"sync", "status"}:
            raise SyncError("action must be sync or status")
        configured_url = request.get("supabase_url")
        if configured_url is not None and (
            not isinstance(configured_url, str) or not configured_url
        ):
            raise SyncError("supabase_url must be a non-empty string when provided")
        base_url = configured_url or os.environ.get("PRACTICE_SUPABASE_URL")
        key = os.environ.get("PRACTICE_SUPABASE_KEY")
        configured = collection_id is not None and isinstance(base_url, str) and bool(base_url)
        status_response["configured"] = configured
        if action == "status":
            status_response["status"] = "ready" if configured else "disabled"
            return status_response
        if not configured:
            return status_response
        parsed = urllib.parse.urlparse(base_url)
        loopback_http = parsed.scheme == "http" and parsed.hostname in {
            "127.0.0.1", "::1", "localhost"
        }
        if (parsed.scheme != "https" and not loopback_http) or not parsed.netloc:
            raise SyncError("supabase_url must be an absolute HTTP(S) URL")
        base_url = base_url.rstrip("/")
        attempted_at = utc_timestamp()
        connection.execute(
            """INSERT INTO sync_metadata(collection_id, bootstrap_state, last_attempt_at)
               VALUES (?, 'uninitialized', ?)
               ON CONFLICT(collection_id) DO UPDATE SET last_attempt_at=excluded.last_attempt_at""",
            (collection_id, attempted_at),
        )
        connection.commit()
        local_rows = connection.execute(
            "SELECT * FROM reviews WHERE collection_key = ? ORDER BY review_datetime, event_id",
            (collection_id,),
        ).fetchall()
        legacy_row = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'legacy_collection_keys'"
        ).fetchone()
        try:
            legacy_keys = json.loads(legacy_row[0]) if legacy_row else []
        except json.JSONDecodeError:
            legacy_keys = []
        legacy = collection_id in legacy_keys
        sync_row = connection.execute(
            "SELECT bootstrap_state, last_remote_sequence FROM sync_metadata "
            "WHERE collection_id = ?",
            (collection_id,),
        ).fetchone()
        bootstrap = sync_row["bootstrap_state"]
        last_remote_sequence = sync_row["last_remote_sequence"]
    finally:
        connection.close()

    if bootstrap == "conflict":
        return {**status_response, "status": "bootstrap_conflict", "pending": pending}

    if not key:
        connection = store.connect()
        try:
            connection.execute(
                "UPDATE sync_metadata SET last_error='credentials unavailable' WHERE collection_id=?",
                (collection_id,),
            )
            connection.commit()
        finally:
            connection.close()
        return {
            **status_response,
            "status": "unavailable",
            "error": "credentials unavailable",
        }

    adapter = adapter or UrllibAdapter()
    try:
        local_ids = {row["event_id"] for row in local_rows}
        local_by_id = {row["event_id"]: remote_event(row, collection_id) for row in local_rows}

        if last_remote_sequence is None:
            remote = fetch_remote(adapter, base_url, key, collection_id, 0)
            remote_ids = {event["event_id"] for event in remote}
            for event in remote:
                if (
                    event["event_id"] in local_by_id
                    and event_payload(event) != local_by_id[event["event_id"]]
                ):
                    raise UnavailableError("remote event conflicts with local event UUID")
            if (
                bootstrap == "uninitialized"
                and legacy
                and local_rows
                and any(event_id not in local_ids for event_id in remote_ids)
            ):
                connection = store.connect()
                try:
                    connection.execute(
                        "UPDATE sync_metadata SET bootstrap_state='conflict', last_error=? "
                        "WHERE collection_id=?",
                        ("bootstrap conflict", collection_id),
                    )
                    connection.commit()
                finally:
                    connection.close()
                return {
                    **status_response,
                    "status": "bootstrap_conflict",
                    "pending": len(local_rows),
                }
            uploads = [
                remote_event(row, collection_id)
                for row in local_rows
                if row["event_id"] not in remote_ids
            ]
            upload_events(adapter, base_url, key, uploads)
            bootstrap_cursor = max(
                (event["sync_sequence"] for event in remote), default=0
            )
            tail = fetch_remote(
                adapter, base_url, key, collection_id, bootstrap_cursor
            )
            if any(event["event_id"] in remote_ids for event in tail):
                raise UnavailableError("remote response contains duplicate event UUIDs")
            remote.extend(tail)
        else:
            uploads = [
                remote_event(row, collection_id)
                for row in local_rows
                if not row["remote_confirmed"]
            ]
            upload_events(adapter, base_url, key, uploads)
            remote = fetch_remote(
                adapter, base_url, key, collection_id, last_remote_sequence
            )

        remote_ids = {event["event_id"] for event in remote}
        for event in remote:
            if (
                event["event_id"] in local_by_id
                and event_payload(event) != local_by_id[event["event_id"]]
            ):
                raise UnavailableError("remote event conflicts with local event UUID")
        downloads = [event for event in remote if event["event_id"] not in local_ids]
        new_cursor = max(
            (event["sync_sequence"] for event in remote),
            default=last_remote_sequence or 0,
        )

        connection = store.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            affected: set[str] = set()
            for event in downloads:
                affected.add(event["exercise_id"])
                reviewed_at = datetime.fromisoformat(event["review_datetime"])
                initial_card = Card(due=reviewed_at)
                connection.execute(
                    """INSERT OR IGNORE INTO cards
                       (collection_key, exercise_id, card_json, due_at, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        collection_id, event["exercise_id"], initial_card.to_json(),
                        reviewed_at.isoformat(), reviewed_at.isoformat(), reviewed_at.isoformat(),
                    ),
                )
                connection.execute(
                    """INSERT INTO reviews
                       (event_id, collection_key, exercise_id, review_datetime, final_rating,
                        compiled, proposed_rating, review_log_json, remote_confirmed,
                        review_status, reviewer_name, reviewer_model,
                        reviewer_reasoning_effort, review_attempts,
                        solve_duration_ms, feedback_duration_ms)
                       VALUES (?, ?, ?, ?, ?, ?, ?, '{}', 1, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        event["event_id"], collection_id, event["exercise_id"],
                        event["review_datetime"], event["final_rating"], int(event["compiled"]),
                        event["proposed_rating"], event["review_status"], event["reviewer_name"],
                        event["reviewer_model"], event["reviewer_reasoning_effort"],
                        event["review_attempts"], event["solve_duration_ms"],
                        event["feedback_duration_ms"],
                    ),
                )
            replay_exercises(connection, collection_id, affected)
            confirmed_ids = remote_ids | {event["event_id"] for event in uploads}
            if confirmed_ids:
                connection.executemany(
                    "UPDATE reviews SET remote_confirmed=1 WHERE event_id=?",
                    ((event_id,) for event_id in confirmed_ids),
                )
            succeeded_at = utc_timestamp()
            connection.execute(
                """UPDATE sync_metadata SET bootstrap_state='initialized',
                   last_success_at=?, last_error=NULL, last_remote_sequence=?
                   WHERE collection_id=?""",
                (succeeded_at, new_cursor, collection_id),
            )
            pending = connection.execute(
                "SELECT count(*) FROM reviews "
                "WHERE collection_key=? AND remote_confirmed=0",
                (collection_id,),
            ).fetchone()[0]
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {
            "status": "success", "configured": True, "uploaded": len(uploads),
            "downloaded": len(downloads), "pending": pending, "last_success": succeeded_at,
        }
    except (UnavailableError, json.JSONDecodeError, UnicodeError) as error:
        safe_error = str(error)[:160] or "synchronization unavailable"
        connection = store.connect()
        try:
            connection.execute(
                "UPDATE sync_metadata SET last_error=? WHERE collection_id=?",
                (safe_error, collection_id),
            )
            connection.commit()
            pending = connection.execute(
                "SELECT count(*) FROM reviews WHERE collection_key=? AND remote_confirmed=0",
                (collection_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        return {
            "status": "unavailable", "configured": True, "pending": pending,
            "error": safe_error, "last_success": status_response["last_success"],
        }


def main() -> int:
    try:
        request = json.load(sys.stdin)
        response = sync_progress(request)
    except (json.JSONDecodeError, SyncError, SchedulerError, sqlite3.Error, OSError) as error:
        response = {"error": str(error)}
        json.dump(response, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
