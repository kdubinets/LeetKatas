#!/usr/bin/env python3
"""Report collection-scoped practice statistics from SQLite and FSRS cards."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date, datetime, timedelta, tzinfo
from pathlib import Path
from typing import Any

from practice_scheduler import (
    PracticeStore,
    RATING_NAMES,
    SchedulerError,
    canonical_collection,
    database_path,
    deserialize_card,
    ensure_utc,
)


class RequestError(ValueError):
    """Raised when a statistics request is invalid."""


def read_request() -> dict[str, Any]:
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise RequestError(f"invalid JSON request: {error.msg}") from error
    if not isinstance(request, dict):
        raise RequestError("request must be a JSON object")
    return request


def required_extension(request: dict[str, Any], name: str) -> str:
    value = request.get(name)
    if not isinstance(value, str) or not value.startswith("."):
        raise RequestError(f"{name} must be a string starting with a dot")
    return value


def local_date(value: datetime, local_zone: tzinfo | None) -> date:
    return value.astimezone(local_zone).date() if local_zone else value.astimezone().date()


def empty_ratings() -> dict[str, int]:
    return {name: 0 for name in ("fail", "acceptable", "good", "excellent")}


def discover_ids(collection: Path, source_extension: str, metadata_extension: str) -> set[str]:
    return {
        source.stem
        for source in collection.glob(f"*{source_extension}")
        if source.is_file() and source.with_suffix(metadata_extension).is_file()
    }


def practice_stats(
    request: dict[str, Any],
    current_datetime: datetime | None = None,
    local_zone: tzinfo | None = None,
) -> dict[str, Any]:
    collection_key = canonical_collection(request.get("exercise_directory"))
    source_extension = required_extension(request, "source_extension")
    metadata_extension = required_extension(request, "metadata_extension")
    history_days = request.get("history_days", 30)
    if type(history_days) is not int or not 1 <= history_days <= 366:
        raise RequestError("history_days must be an integer between 1 and 366")

    now = ensure_utc(current_datetime)
    today = local_date(now, local_zone)
    tomorrow = today + timedelta(days=1)
    active_ids = discover_ids(Path(collection_key), source_extension, metadata_extension)

    store = PracticeStore(database_path(request))
    connection = store.connect()
    try:
        card_rows = connection.execute(
            "SELECT exercise_id, card_json FROM cards WHERE collection_key = ?",
            (collection_key,),
        ).fetchall()
        review_rows = connection.execute(
            """SELECT exercise_id, review_datetime, final_rating,
                      solve_duration_ms, feedback_duration_ms
               FROM reviews WHERE collection_key = ? ORDER BY review_datetime""",
            (collection_key,),
        ).fetchall()
    finally:
        connection.close()

    cards = {
        row["exercise_id"]: deserialize_card(row["card_json"])
        for row in card_rows
        if row["exercise_id"] in active_ids
    }
    state_counts = {"learning": 0, "learned": 0, "relearning": 0}
    due_now = 0
    due_later_today = 0
    forecast_dates = [tomorrow + timedelta(days=offset) for offset in range(7)]
    forecast_counts = {day: 0 for day in forecast_dates}
    for card in cards.values():
        state_name = card.state.name.lower()
        if state_name in {"new", "learning"}:
            state_counts["learning"] += 1
        elif state_name == "review":
            state_counts["learned"] += 1
        elif state_name == "relearning":
            state_counts["relearning"] += 1

        if card.due <= now:
            due_now += 1
            continue
        due_date = local_date(card.due, local_zone)
        if due_date == today:
            due_later_today += 1
        if due_date in forecast_counts:
            forecast_counts[due_date] += 1

    history_dates = [today - timedelta(days=offset) for offset in range(history_days - 1, -1, -1)]
    history = {
        day: {
            "date": day.isoformat(),
            "reviews": 0,
            "new_introduced": 0,
            "ratings": empty_ratings(),
            "practice_time_ms": 0,
            "tracked_reviews": 0,
        }
        for day in history_dates
    }
    first_review_dates: dict[str, date] = {}
    for row in review_rows:
        reviewed_at = datetime.fromisoformat(row["review_datetime"])
        reviewed_date = local_date(reviewed_at, local_zone)
        first_review_dates.setdefault(row["exercise_id"], reviewed_date)
        day = history.get(reviewed_date)
        if day is None:
            continue
        day["reviews"] += 1
        rating = row["final_rating"]
        if rating in RATING_NAMES:
            day["ratings"][rating] += 1
        solve_ms = row["solve_duration_ms"]
        feedback_ms = row["feedback_duration_ms"]
        if solve_ms is not None and feedback_ms is not None:
            day["practice_time_ms"] += solve_ms + feedback_ms
            day["tracked_reviews"] += 1

    for introduced_date in first_review_dates.values():
        if introduced_date in history:
            history[introduced_date]["new_introduced"] += 1

    today_stats = history[today]
    return {
        "collection": collection_key,
        "generated_at": now.isoformat(),
        "today": {
            **today_stats,
            "due_now": due_now,
            "due_later_today": due_later_today,
        },
        "collection_state": {
            "total": len(active_ids),
            "unseen": len(active_ids - cards.keys()),
            "introduced": len(cards),
            **state_counts,
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
        response = practice_stats(read_request())
    except (OSError, RequestError, SchedulerError, sqlite3.Error, UnicodeError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
