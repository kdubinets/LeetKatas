#!/usr/bin/env python3
"""Report Level C scheduling, review, hint, and bookmark statistics."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date, datetime, timedelta, tzinfo
from typing import Any

from practice_scheduler import RATING_NAMES, SchedulerError, ensure_utc
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def local_date(value: datetime, local_zone: tzinfo | None) -> date:
    return value.astimezone(local_zone).date() if local_zone else value.astimezone().date()


def problem_solving_stats(
    request: dict[str, Any],
    current_datetime: datetime | None = None,
    local_zone: tzinfo | None = None,
) -> dict[str, Any]:
    _, collection_key, problem_ids = problem_collection(request.get("collection_directory"))
    history_days = request.get("history_days", 30)
    if type(history_days) is not int or not 1 <= history_days <= 366:
        raise RequestError("history_days must be an integer between 1 and 366")
    now = ensure_utc(current_datetime)
    today = local_date(now, local_zone)
    tomorrow = today + timedelta(days=1)
    store = ProblemSolvingStore(problem_solving_database_path(request))
    cards = store.cards_for_collection(collection_key)
    bookmarks = store.list_bookmarks(collection_key)
    active_ids = set(problem_ids)
    bookmarked_ids = {bookmark["problem_id"] for bookmark in bookmarks}
    connection = store.connect()
    try:
        rows = connection.execute(
            """SELECT problem_id, review_datetime, final_rating, hint_used,
                      clarification_used, solve_duration_ms, discussion_duration_ms
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
    active_cards = {
        problem_id: card for problem_id, card in cards.items() if problem_id in active_ids
    }
    introduced = set(active_cards)
    due_now = sum(
        1
        for problem_id in introduced - bookmarked_ids
        if active_cards[problem_id].due <= now
    )
    due_later_today = sum(
        1
        for problem_id in introduced - bookmarked_ids
        if active_cards[problem_id].due > now
        and local_date(active_cards[problem_id].due, local_zone) == today
    )
    state_counts = {"learning": 0, "learned": 0, "relearning": 0}
    forecast_dates = [tomorrow + timedelta(days=offset) for offset in range(7)]
    forecast_counts = {day: 0 for day in forecast_dates}
    for problem_id, card in active_cards.items():
        state_name = card.state.name.lower()
        if state_name in {"new", "learning"}:
            state_counts["learning"] += 1
        elif state_name == "review":
            state_counts["learned"] += 1
        elif state_name == "relearning":
            state_counts["relearning"] += 1
        if problem_id in bookmarked_ids or card.due <= now:
            continue
        due_date = local_date(card.due, local_zone)
        if due_date in forecast_counts:
            forecast_counts[due_date] += 1

    ratings = {name: 0 for name in RATING_NAMES}
    history_dates = [
        today - timedelta(days=offset) for offset in range(history_days - 1, -1, -1)
    ]
    history = {
        day: {
            "date": day.isoformat(),
            "reviews": 0,
            "new_reviewed": 0,
            "ratings": {name: 0 for name in RATING_NAMES},
            "practice_time_ms": 0,
        }
        for day in history_dates
    }
    first_review_dates: dict[str, date] = {}
    for row in rows:
        rating = row["final_rating"]
        if rating in ratings:
            ratings[rating] += 1
        review_date = local_date(
            datetime.fromisoformat(row["review_datetime"]), local_zone
        )
        first_review_dates.setdefault(row["problem_id"], review_date)
        day = history.get(review_date)
        if day is not None:
            day["reviews"] += 1
            if rating in day["ratings"]:
                day["ratings"][rating] += 1
            day["practice_time_ms"] += row["solve_duration_ms"] + row["discussion_duration_ms"]
    for first_review_date in first_review_dates.values():
        if first_review_date in history:
            history[first_review_date]["new_reviewed"] += 1
    today_stats = history[today]
    return {
        "collection": collection_key,
        "generated_at": now.isoformat(),
        "collection_state": {
            "total": len(active_ids),
            "unseen": len(active_ids - active_cards.keys()),
            "introduced": len(introduced),
            "due_now": due_now,
            "open_bookmarks": len(bookmarks),
            **state_counts,
        },
        "today": {
            **today_stats,
            "due_now": due_now,
            "due_later_today": due_later_today,
        },
        "reviews": {
            "total": len(rows),
            "problems_total": len({row["problem_id"] for row in rows}),
            "ratings": ratings,
            "hint_used": sum(row["hint_used"] for row in rows),
            "clarification_used": sum(row["clarification_used"] for row in rows),
            "revealed": len(rows) + unrated_reveals,
            "revealed_unrated": unrated_reveals,
            "solve_time_ms": sum(row["solve_duration_ms"] for row in rows),
            "discussion_time_ms": sum(row["discussion_duration_ms"] for row in rows),
        },
        "bookmarks": {
            "open": len(bookmarks),
            "lifecycle_events": {row["action"]: row["count"] for row in lifecycle},
        },
        "forecast": {
            "tomorrow_due": forecast_counts[tomorrow],
            "days": [
                {"date": day.isoformat(), "due": forecast_counts[day]}
                for day in forecast_dates
            ],
        },
        "history": [history[day] for day in reversed(history_dates)],
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
