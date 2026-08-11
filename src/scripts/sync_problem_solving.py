#!/usr/bin/env python3
"""Synchronize Level C reviews, bookmarks, and opt-in private artifacts."""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import urllib.parse
import uuid
from datetime import datetime, timezone
from typing import Any

from level_c_conversation_protocol import ConversationError, validate_history
from practice_scheduler import Card, RATING_NAMES, SchedulerError, collection_keys
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
    replay_problem_cards,
)
from sync_progress import (
    HttpAdapter,
    UnavailableError,
    UrllibAdapter,
    check_status,
    headers,
    utc_timestamp,
)


PAGE_SIZE = 200
UPLOAD_BATCH_SIZE = 100
STREAMS = {
    "review": (
        "problem_solving_review_events",
        "review_cursor",
        "sync_sequence,event_id,collection_id,problem_id,review_datetime,"
        "final_rating,hint_used,clarification_used,solve_duration_ms,"
        "discussion_duration_ms",
    ),
    "bookmark": (
        "problem_solving_bookmark_events",
        "bookmark_cursor",
        "sync_sequence,event_id,collection_id,problem_id,revision,action,event_datetime",
    ),
    "artifact": (
        "problem_solving_artifact_events",
        "artifact_cursor",
        "sync_sequence,event_id,collection_id,problem_id,revision,updated_at,artifact_json",
    ),
}


class SyncError(ValueError):
    pass


def required_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 512:
        raise UnavailableError(f"remote event has invalid {name}")
    return value


def canonical_uuid(value: Any) -> str:
    text = required_text(value, "event_id")
    try:
        parsed = uuid.UUID(text)
    except ValueError as error:
        raise UnavailableError("remote event has invalid event_id") from error
    if str(parsed) != text:
        raise UnavailableError("remote event has non-canonical event_id")
    return text


def utc_datetime(value: Any, name: str) -> str:
    text = required_text(value, name)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as error:
        raise UnavailableError(f"remote event has invalid {name}") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise UnavailableError(f"remote event {name} must be UTC")
    return parsed.isoformat()


def common_event(value: Any, collection_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise UnavailableError("remote response contains a non-object event")
    sequence = value.get("sync_sequence")
    if type(sequence) is not int or sequence <= 0:
        raise UnavailableError("remote event has invalid sync_sequence")
    if value.get("collection_id") != collection_id:
        raise UnavailableError("remote event has an unexpected collection_id")
    return {
        "sync_sequence": sequence,
        "event_id": canonical_uuid(value.get("event_id")),
        "collection_id": collection_id,
        "problem_id": required_text(value.get("problem_id"), "problem_id"),
    }


def validate_remote_event(
    stream: str, value: Any, collection_id: str
) -> dict[str, Any]:
    event = common_event(value, collection_id)
    if stream == "review":
        rating = value.get("final_rating")
        if rating not in RATING_NAMES:
            raise UnavailableError("remote review has invalid final_rating")
        event.update(
            review_datetime=utc_datetime(value.get("review_datetime"), "review_datetime"),
            final_rating=rating,
        )
        for name in ("hint_used", "clarification_used"):
            if not isinstance(value.get(name), bool):
                raise UnavailableError(f"remote review has invalid {name}")
            event[name] = value[name]
        for name in ("solve_duration_ms", "discussion_duration_ms"):
            duration = value.get(name)
            if type(duration) is not int or duration < 0:
                raise UnavailableError(f"remote review has invalid {name}")
            event[name] = duration
    elif stream == "bookmark":
        revision = value.get("revision")
        action = value.get("action")
        if type(revision) is not int or revision <= 0:
            raise UnavailableError("remote bookmark has invalid revision")
        if action not in {"create", "update", "remove"}:
            raise UnavailableError("remote bookmark has invalid action")
        event.update(
            revision=revision,
            action=action,
            event_datetime=utc_datetime(value.get("event_datetime"), "event_datetime"),
        )
    else:
        revision = value.get("revision")
        artifact = value.get("artifact_json")
        if type(revision) is not int or revision <= 0:
            raise UnavailableError("remote artifact has invalid revision")
        if not isinstance(artifact, dict):
            raise UnavailableError("remote artifact has invalid artifact_json")
        # Accept legacy artifact events long enough to synchronize them, but
        # discard the retired field before storing the current representation.
        artifact.pop("gave_up", None)
        expected = {
            "hint_requested", "clarification_used", "revealed",
            "selected_at", "revealed_at", "note", "conversation_history",
        }
        if set(artifact) != expected:
            raise UnavailableError("remote artifact has invalid artifact_json fields")
        for name in ("hint_requested", "clarification_used", "revealed"):
            if not isinstance(artifact[name], bool):
                raise UnavailableError(f"remote artifact has invalid {name}")
        if artifact["note"] is not None and not isinstance(artifact["note"], str):
            raise UnavailableError("remote artifact has invalid note")
        artifact["selected_at"] = utc_datetime(
            artifact["selected_at"], "artifact selected_at"
        )
        if artifact["revealed_at"] is not None:
            artifact["revealed_at"] = utc_datetime(
                artifact["revealed_at"], "artifact revealed_at"
            )
        try:
            artifact["conversation_history"] = validate_history(
                artifact["conversation_history"]
            )
        except ConversationError as error:
            raise UnavailableError(
                "remote artifact has invalid conversation_history"
            ) from error
        event.update(
            revision=revision,
            updated_at=utc_datetime(value.get("updated_at"), "updated_at"),
            artifact_json=artifact,
        )
    return event


def fetch_stream(
    adapter: HttpAdapter,
    base_url: str,
    key: str,
    collection_id: str,
    stream: str,
    cursor: int,
) -> list[dict[str, Any]]:
    table, _, fields = STREAMS[stream]
    events: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    encoded = urllib.parse.quote(collection_id, safe="")
    while True:
        query = (
            f"collection_id=eq.{encoded}&select={fields}&sync_sequence=gt.{cursor}"
            f"&order=sync_sequence.asc&limit={PAGE_SIZE}"
        )
        status, body = adapter.request(
            "GET", f"{base_url}/rest/v1/{table}?{query}", headers(key), None
        )
        if status == 400:
            raise UnavailableError("remote sync schema is outdated; rerun supabase_setup.sql")
        check_status(status)
        try:
            page = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise UnavailableError("remote service returned malformed JSON") from error
        if not isinstance(page, list):
            raise UnavailableError("remote service returned an invalid event page")
        validated = [validate_remote_event(stream, item, collection_id) for item in page]
        sequences = [item["sync_sequence"] for item in validated]
        if sequences != sorted(sequences) or any(sequence <= cursor for sequence in sequences):
            raise UnavailableError("remote response contains unordered sync sequences")
        if len(sequences) != len(set(sequences)):
            raise UnavailableError("remote response contains duplicate sync sequences")
        page_ids = {item["event_id"] for item in validated}
        if len(page_ids) != len(validated) or page_ids & event_ids:
            raise UnavailableError("remote response contains duplicate event UUIDs")
        events.extend(validated)
        event_ids.update(page_ids)
        if validated:
            cursor = validated[-1]["sync_sequence"]
        if len(page) < PAGE_SIZE:
            return events


def upload_stream(
    adapter: HttpAdapter,
    base_url: str,
    key: str,
    stream: str,
    events: list[dict[str, Any]],
) -> None:
    table = STREAMS[stream][0]
    for start in range(0, len(events), UPLOAD_BATCH_SIZE):
        body = json.dumps(
            events[start : start + UPLOAD_BATCH_SIZE], separators=(",", ":")
        ).encode()
        status, _ = adapter.request(
            "POST",
            f"{base_url}/rest/v1/{table}?on_conflict=event_id",
            headers(key, "resolution=ignore-duplicates,return=minimal"),
            body,
        )
        check_status(status)


def review_payload(row: sqlite3.Row, collection_id: str) -> dict[str, Any]:
    return {
        "event_id": row["event_id"], "collection_id": collection_id,
        "problem_id": row["problem_id"], "review_datetime": row["review_datetime"],
        "final_rating": row["final_rating"], "hint_used": bool(row["hint_used"]),
        "clarification_used": bool(row["clarification_used"]),
        "solve_duration_ms": row["solve_duration_ms"],
        "discussion_duration_ms": row["discussion_duration_ms"],
    }


def bookmark_payload(row: sqlite3.Row, collection_id: str) -> dict[str, Any]:
    return {
        "event_id": row["event_id"], "collection_id": collection_id,
        "problem_id": row["problem_id"], "revision": row["revision"],
        "action": row["action"], "event_datetime": row["event_datetime"],
    }


def artifact_payload(row: sqlite3.Row, collection_id: str) -> dict[str, Any]:
    return {
        "event_id": row["event_id"], "collection_id": collection_id,
        "problem_id": row["problem_id"], "revision": row["revision"],
        "updated_at": row["updated_at"],
        "artifact_json": {
            "hint_requested": bool(row["hint_requested"]),
            "clarification_used": bool(row["clarification_used"]),
            "revealed": bool(row["revealed"]),
            "selected_at": row["selected_at"], "revealed_at": row["revealed_at"],
            "note": row["note"],
            "conversation_history": json.loads(row["conversation_json"]),
        },
    }


def immutable_payload(event: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in event.items() if key != "sync_sequence"}


def rebuild_bookmark(
    connection: sqlite3.Connection, collection_id: str, problem_id: str
) -> None:
    rows = connection.execute(
        """SELECT * FROM problem_solving_bookmark_events
           WHERE collection_key=? AND problem_id=?
           ORDER BY revision, event_datetime, event_id""",
        (collection_id, problem_id),
    ).fetchall()
    bookmarked_at: str | None = None
    for row in rows:
        if row["action"] == "create":
            bookmarked_at = row["event_datetime"]
        elif bookmarked_at is None and row["action"] == "update":
            bookmarked_at = row["event_datetime"]
        if row["action"] == "remove":
            bookmarked_at = None
    winner = rows[-1]
    connection.execute(
        """INSERT INTO problem_solving_bookmarks
           (collection_key, problem_id, revision, bookmarked_at, updated_at, removed_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(collection_key, problem_id) DO UPDATE SET
             revision=excluded.revision, bookmarked_at=excluded.bookmarked_at,
             updated_at=excluded.updated_at, removed_at=excluded.removed_at""",
        (
            collection_id, problem_id, winner["revision"],
            bookmarked_at or winner["event_datetime"], winner["event_datetime"],
            winner["event_datetime"] if winner["action"] == "remove" else None,
        ),
    )


def sync_problem_solving(
    request: dict[str, Any], adapter: HttpAdapter | None = None
) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise SyncError("request must be a JSON object")
    _, collection_key, problem_ids = problem_collection(
        request.get("collection_directory")
    )
    _, _, collection_id = collection_keys(request.get("collection_directory"))
    if collection_id is None:
        raise SyncError("collection requires a stable collection identity")
    private_sync = request.get("private_content_sync", False)
    if not isinstance(private_sync, bool):
        raise SyncError("private_content_sync must be a boolean")
    action = request.get("action", "sync")
    if action not in {"sync", "status"}:
        raise SyncError("action must be sync or status")
    configured_url = request.get("supabase_url")
    if configured_url is not None and (not isinstance(configured_url, str) or not configured_url):
        raise SyncError("supabase_url must be a non-empty string when provided")
    base_url = configured_url or os.environ.get("PROBLEM_SOLVING_SUPABASE_URL")
    key = os.environ.get("PROBLEM_SOLVING_SUPABASE_KEY") or os.environ.get("PRACTICE_SUPABASE_KEY")
    configured = isinstance(base_url, str) and bool(base_url)
    store = ProblemSolvingStore(problem_solving_database_path(request))
    connection = store.connect()
    try:
        pending_reviews = connection.execute(
            "SELECT count(*) FROM problem_solving_reviews WHERE collection_key=? AND remote_confirmed=0",
            (collection_key,),
        ).fetchone()[0]
        pending_bookmarks = connection.execute(
            "SELECT count(*) FROM problem_solving_bookmark_events WHERE collection_key=? AND remote_confirmed=0",
            (collection_key,),
        ).fetchone()[0]
        pending_artifacts = connection.execute(
            "SELECT count(*) FROM problem_solving_artifacts WHERE collection_key=? AND remote_confirmed=0",
            (collection_key,),
        ).fetchone()[0] if private_sync else 0
        metadata = connection.execute(
            "SELECT * FROM problem_solving_sync_metadata WHERE collection_id=?",
            (collection_id,),
        ).fetchone()
    finally:
        connection.close()
    status = {
        "status": "ready" if configured else "disabled", "configured": configured,
        "private_content_sync": private_sync,
        "pending": {
            "reviews": pending_reviews, "bookmarks": pending_bookmarks,
            "artifacts": pending_artifacts,
        },
        "last_success": metadata["last_success_at"] if metadata else None,
    }
    if action == "status" or not configured:
        return status
    parsed = urllib.parse.urlparse(base_url)
    loopback = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "::1", "localhost"}
    if (parsed.scheme != "https" and not loopback) or not parsed.netloc:
        raise SyncError("supabase_url must be an absolute HTTP(S) URL")
    if not key:
        return {**status, "status": "unavailable", "error": "credentials unavailable"}
    base_url = base_url.rstrip("/")
    adapter = adapter or UrllibAdapter()
    active_streams = ["review", "bookmark"] + (["artifact"] if private_sync else [])
    try:
        connection = store.connect()
        try:
            connection.execute(
                """INSERT INTO problem_solving_sync_metadata(collection_id, last_attempt_at)
                   VALUES (?, ?) ON CONFLICT(collection_id) DO UPDATE SET
                   last_attempt_at=excluded.last_attempt_at""",
                (collection_id, utc_timestamp()),
            )
            connection.commit()
            metadata = connection.execute(
                "SELECT * FROM problem_solving_sync_metadata WHERE collection_id=?",
                (collection_id,),
            ).fetchone()
            rows = {
                "review": connection.execute(
                    "SELECT * FROM problem_solving_reviews WHERE collection_key=?",
                    (collection_id,),
                ).fetchall(),
                "bookmark": connection.execute(
                    "SELECT * FROM problem_solving_bookmark_events WHERE collection_key=?",
                    (collection_id,),
                ).fetchall(),
                "artifact": connection.execute(
                    "SELECT * FROM problem_solving_artifacts WHERE collection_key=?",
                    (collection_id,),
                ).fetchall(),
            }
        finally:
            connection.close()
        payload_builder = {
            "review": review_payload, "bookmark": bookmark_payload,
            "artifact": artifact_payload,
        }
        uploaded: dict[str, list[dict[str, Any]]] = {}
        remote: dict[str, list[dict[str, Any]]] = {}
        for stream in active_streams:
            local = [payload_builder[stream](row, collection_id) for row in rows[stream]]
            uploaded[stream] = [
                payload_builder[stream](row, collection_id)
                for row in rows[stream] if not row["remote_confirmed"]
            ]
            upload_stream(adapter, base_url, key, stream, uploaded[stream])
            remote[stream] = fetch_stream(
                adapter, base_url, key, collection_id, stream,
                metadata[STREAMS[stream][1]],
            )
            if any(event["problem_id"] not in problem_ids for event in remote[stream]):
                raise UnavailableError(
                    f"remote {stream} event references an unknown problem_id"
                )
            local_by_id = {event["event_id"]: event for event in local}
            for event in remote[stream]:
                if event["event_id"] in local_by_id and immutable_payload(event) != local_by_id[event["event_id"]]:
                    raise UnavailableError(f"remote {stream} event conflicts with local event UUID")

        connection = store.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            affected_reviews: set[str] = set()
            affected_bookmarks: set[str] = set()
            downloads = {stream: 0 for stream in active_streams}
            local_ids = {
                stream: {row["event_id"] for row in rows[stream]} for stream in active_streams
            }
            for event in remote.get("review", []):
                if event["event_id"] in local_ids["review"]:
                    continue
                affected_reviews.add(event["problem_id"])
                initial = Card(due=datetime.fromisoformat(event["review_datetime"]))
                connection.execute(
                    """INSERT OR IGNORE INTO problem_solving_cards
                       (collection_key, problem_id, card_json, due_at, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (collection_id, event["problem_id"], initial.to_json(), event["review_datetime"], event["review_datetime"], event["review_datetime"]),
                )
                connection.execute(
                    """INSERT INTO problem_solving_reviews
                       (event_id, collection_key, problem_id, review_datetime, final_rating,
                        review_log_json, hint_used, clarification_used,
                        solve_duration_ms, discussion_duration_ms, remote_confirmed)
                       VALUES (?, ?, ?, ?, ?, '{}', ?, ?, ?, ?, 1)""",
                    (event["event_id"], collection_id, event["problem_id"], event["review_datetime"], event["final_rating"], int(event["hint_used"]), int(event["clarification_used"]), event["solve_duration_ms"], event["discussion_duration_ms"]),
                )
                downloads["review"] += 1
            replay_problem_cards(connection, collection_id, affected_reviews)
            for event in remote.get("bookmark", []):
                if event["event_id"] in local_ids["bookmark"]:
                    continue
                connection.execute(
                    """INSERT INTO problem_solving_bookmark_events
                       (event_id, collection_key, problem_id, revision, action,
                        event_datetime, remote_confirmed) VALUES (?, ?, ?, ?, ?, ?, 1)""",
                    (event["event_id"], collection_id, event["problem_id"], event["revision"], event["action"], event["event_datetime"]),
                )
                affected_bookmarks.add(event["problem_id"])
                downloads["bookmark"] += 1
            for problem_id in affected_bookmarks:
                rebuild_bookmark(connection, collection_id, problem_id)
            for event in remote.get("artifact", []):
                artifact = event["artifact_json"]
                if artifact["revealed"] and artifact["revealed_at"] is not None:
                    bookmarked = connection.execute(
                        "SELECT 1 FROM problem_solving_bookmarks "
                        "WHERE collection_key=? AND problem_id=? AND removed_at IS NULL",
                        (collection_id, event["problem_id"]),
                    ).fetchone()
                    reviewed = connection.execute(
                        "SELECT 1 FROM problem_solving_reviews "
                        "WHERE collection_key=? AND problem_id=? AND review_datetime>=? LIMIT 1",
                        (collection_id, event["problem_id"], artifact["revealed_at"]),
                    ).fetchone()
                    if bookmarked is None and reviewed is not None:
                        continue
                current = connection.execute(
                    "SELECT * FROM problem_solving_artifacts WHERE collection_key=? AND problem_id=?",
                    (collection_id, event["problem_id"]),
                ).fetchone()
                remote_key = (event["revision"], event["updated_at"], event["event_id"])
                local_key = (current["revision"], current["updated_at"], current["event_id"]) if current else None
                if local_key is not None and remote_key <= local_key:
                    continue
                connection.execute(
                    """INSERT INTO problem_solving_artifacts
                       (collection_key, problem_id, event_id, revision, hint_requested,
                        clarification_used, revealed, selected_at,
                        revealed_at, note, conversation_json, updated_at,
                        remote_confirmed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                       ON CONFLICT(collection_key, problem_id) DO UPDATE SET
                         event_id=excluded.event_id, revision=excluded.revision,
                         hint_requested=excluded.hint_requested,
                         clarification_used=excluded.clarification_used,
                         revealed=excluded.revealed,
                         selected_at=excluded.selected_at,
                         revealed_at=excluded.revealed_at,
                         note=excluded.note, conversation_json=excluded.conversation_json,
                         updated_at=excluded.updated_at, remote_confirmed=1""",
                    (collection_id, event["problem_id"], event["event_id"], event["revision"], int(artifact["hint_requested"]), int(artifact["clarification_used"]), int(artifact["revealed"]), artifact["selected_at"], artifact["revealed_at"], artifact["note"], json.dumps(artifact["conversation_history"], ensure_ascii=False, separators=(",", ":")), event["updated_at"]),
                )
                downloads["artifact"] += 1
            for stream in active_streams:
                table = {"review": "problem_solving_reviews", "bookmark": "problem_solving_bookmark_events", "artifact": "problem_solving_artifacts"}[stream]
                connection.executemany(
                    f"UPDATE {table} SET remote_confirmed=1 WHERE event_id=?",
                    ((event["event_id"],) for event in uploaded[stream]),
                )
                cursor = max((event["sync_sequence"] for event in remote[stream]), default=metadata[STREAMS[stream][1]])
                connection.execute(
                    f"UPDATE problem_solving_sync_metadata SET {STREAMS[stream][1]}=? WHERE collection_id=?",
                    (cursor, collection_id),
                )
            succeeded = utc_timestamp()
            connection.execute(
                "UPDATE problem_solving_sync_metadata SET last_success_at=?, last_error=NULL WHERE collection_id=?",
                (succeeded, collection_id),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {
            **status, "status": "success", "last_success": succeeded,
            "uploaded": {stream: len(uploaded[stream]) for stream in active_streams},
            "downloaded": downloads,
            "pending": {"reviews": 0, "bookmarks": 0, "artifacts": 0},
        }
    except (UnavailableError, json.JSONDecodeError, UnicodeError) as error:
        safe = str(error)[:160] or "synchronization unavailable"
        connection = store.connect()
        try:
            connection.execute(
                "UPDATE problem_solving_sync_metadata SET last_error=? WHERE collection_id=?",
                (safe, collection_id),
            )
            connection.commit()
        finally:
            connection.close()
        return {**status, "status": "unavailable", "error": safe}


def main() -> int:
    try:
        request = json.load(sys.stdin)
        response = sync_problem_solving(request)
    except (json.JSONDecodeError, OSError, UnicodeError, SyncError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
