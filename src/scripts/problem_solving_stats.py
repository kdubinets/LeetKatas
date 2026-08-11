#!/usr/bin/env python3
"""Report Level C scheduling, review, hint, and bookmark statistics."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date, datetime
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
    today = now.astimezone().date()
    store = ProblemSolvingStore(problem_solving_database_path(request))
    cards = store.cards_for_collection(collection_key)
    bookmarks = store.list_bookmarks(collection_key)
    active_ids = set(problem_ids)
    bookmarked_ids = {bookmark["problem_id"] for bookmark in bookmarks}
    connection = store.connect()
    try:
        rows = connection.execute(
            """SELECT problem_id, review_datetime, final_rating, hint_used,
                      clarification_used, gave_up, solve_duration_ms, discussion_duration_ms
               FROM problem_solving_reviews WHERE collection_key=? ORDER BY review_datetime""",
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
    due_later_today = sum(
        1
        for problem_id in introduced - bookmarked_ids
        if cards[problem_id].due > now and cards[problem_id].due.astimezone().date() == today
    )
    ratings = {name: 0 for name in RATING_NAMES}
    reviews_today = 0
    first_review_dates: dict[str, date] = {}
    for row in rows:
        ratings[row["final_rating"]] += 1
        review_date = datetime.fromisoformat(row["review_datetime"]).astimezone().date()
        first_review_dates.setdefault(row["problem_id"], review_date)
        if review_date == today:
            reviews_today += 1
    new_reviewed_today = sum(1 for date in first_review_dates.values() if date == today)
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
        "today": {
            "reviews": reviews_today,
            "new_reviewed": new_reviewed_today,
            "due_now": due_now,
            "due_later_today": due_later_today,
        },
        "reviews": {
            "total": len(rows),
            "problems_total": len({row["problem_id"] for row in rows}),
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
