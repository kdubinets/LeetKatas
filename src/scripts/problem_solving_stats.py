#!/usr/bin/env python3
"""Report Level C scheduling, review, hint, and bookmark statistics."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from typing import Any

from practice_scheduler import RATING_NAMES, SchedulerError, ensure_utc
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def problem_solving_stats(
    request: dict[str, Any], current_datetime: datetime | None = None
) -> dict[str, Any]:
    _, collection_key, problem_ids = problem_collection(request.get("collection_directory"))
    now = ensure_utc(current_datetime)
    store = ProblemSolvingStore(problem_solving_database_path(request))
    cards = store.cards_for_collection(collection_key)
    bookmarks = store.list_bookmarks(collection_key)
    active_ids = set(problem_ids)
    bookmarked_ids = {bookmark["problem_id"] for bookmark in bookmarks}
    connection = store.connect()
    try:
        rows = connection.execute(
            """SELECT final_rating, hint_used, clarification_used, gave_up,
                      solve_duration_ms, discussion_duration_ms
               FROM problem_solving_reviews WHERE collection_key=?""",
            (collection_key,),
        ).fetchall()
        lifecycle = connection.execute(
            """SELECT action, count(*) AS count
               FROM problem_solving_bookmark_events WHERE collection_key=?
               GROUP BY action""",
            (collection_key,),
        ).fetchall()
        unrated_reveals = connection.execute(
            """SELECT count(*)
               FROM problem_solving_artifacts a
               WHERE a.collection_key=? AND a.revealed=1
                 AND NOT EXISTS (
                   SELECT 1 FROM problem_solving_reviews r
                   WHERE r.collection_key=a.collection_key
                     AND r.problem_id=a.problem_id
                     AND r.review_datetime >= a.revealed_at
                 )""",
            (collection_key,),
        ).fetchone()[0]
    finally:
        connection.close()
    introduced = active_ids & cards.keys()
    due_now = sum(
        1
        for problem_id in introduced - bookmarked_ids
        if cards[problem_id].due <= now
    )
    ratings = {name: 0 for name in RATING_NAMES}
    for row in rows:
        ratings[row["final_rating"]] += 1
    return {
        "collection": collection_key,
        "generated_at": now.isoformat(),
        "collection_state": {
            "total": len(active_ids),
            "unseen": len(active_ids - cards.keys()),
            "introduced": len(introduced),
            "due_now": due_now,
            "open_bookmarks": len(bookmarks),
        },
        "reviews": {
            "total": len(rows),
            "ratings": ratings,
            "hint_used": sum(row["hint_used"] for row in rows),
            "clarification_used": sum(row["clarification_used"] for row in rows),
            "gave_up": sum(row["gave_up"] for row in rows),
            "revealed": len(rows) + unrated_reveals,
            "revealed_unrated": unrated_reveals,
            "solve_time_ms": sum(row["solve_duration_ms"] for row in rows),
            "discussion_time_ms": sum(row["discussion_duration_ms"] for row in rows),
        },
        "bookmarks": {
            "open": len(bookmarks),
            "lifecycle_events": {row["action"]: row["count"] for row in lifecycle},
        },
    }


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = problem_solving_stats(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
