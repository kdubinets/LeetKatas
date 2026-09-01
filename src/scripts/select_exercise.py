#!/usr/bin/env python3
"""Select a due or ordered-unseen exercise from a collection directory."""

from __future__ import annotations

import json
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from practice_scheduler import (
    PracticeStore,
    SchedulerError,
    collection_keys,
    database_path,
    ensure_utc,
)
from practice_environment import TargetEnvironmentError, load_collection_environment


class RequestError(ValueError):
    """Raised when a script request is invalid."""


def read_request() -> dict[str, Any]:
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise RequestError(f"invalid JSON request: {error.msg}") from error
    if not isinstance(request, dict):
        raise RequestError("request must be a JSON object")
    return request


def required_string(request: dict[str, Any], name: str) -> str:
    value = request.get(name)
    if not isinstance(value, str) or not value:
        raise RequestError(f"{name} must be a non-empty string")
    return value


def collection_directories(request: dict[str, Any]) -> list[str]:
    """Return one or more collection directories from either supported request form."""
    directories = request.get("exercise_directories")
    if directories is None:
        return [required_string(request, "exercise_directory")]
    if "exercise_directory" in request:
        raise RequestError("exercise_directory and exercise_directories cannot both be set")
    if (not isinstance(directories, list) or not directories
            or any(not isinstance(item, str) or not item for item in directories)):
        raise RequestError("exercise_directories must be a non-empty list of strings")
    return directories


def max_new_problems_per_day(request: dict[str, Any]) -> int | None:
    """Return an optional portfolio-wide cap on first-time introductions."""
    value = request.get("new_problems_per_day")
    if value is None:
        return None
    if type(value) is not int or value < 0:
        raise RequestError("new_problems_per_day must be a non-negative integer")
    return value


def introductions_today(
    store: PracticeStore, collection_keys: list[str], now: datetime
) -> int:
    """Count cards whose first recorded review falls on the local current day."""
    placeholders = ", ".join("?" for _ in collection_keys)
    connection = store.connect()
    try:
        rows = connection.execute(
            f"""
            SELECT MIN(review_datetime) AS first_review
            FROM reviews
            WHERE collection_key IN ({placeholders})
            GROUP BY collection_key, exercise_id
            """,
            collection_keys,
        ).fetchall()
    finally:
        connection.close()
    today = now.astimezone().date()
    return sum(
        datetime.fromisoformat(row["first_review"]).astimezone().date() == today
        for row in rows
    )


def next_new_problem_time(now: datetime) -> datetime:
    """Return the next local midnight, when a daily introduction cap resets."""
    local_now = now.astimezone()
    return (local_now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def exercise_order(
    collection: Path, exercises: list[dict[str, Any]]
) -> list[str] | None:
    order_file = collection / "exercise_order.md"
    if not order_file.is_file():
        return None

    ordered_ids = order_file.read_text(encoding="utf-8").splitlines()
    if not ordered_ids:
        raise RequestError(f"exercise order contains no exercises: {order_file}")
    for line_number, exercise_id in enumerate(ordered_ids, start=1):
        if not exercise_id or any(
            character not in "abcdefghijklmnopqrstuvwxyz0123456789_"
            for character in exercise_id
        ):
            raise RequestError(
                f"invalid exercise ID in {order_file} at line {line_number}"
            )

    duplicate_ids = sorted(
        exercise_id
        for exercise_id in set(ordered_ids)
        if ordered_ids.count(exercise_id) > 1
    )
    if duplicate_ids:
        raise RequestError(
            "exercise order contains duplicate exercises: "
            + ", ".join(duplicate_ids)
        )

    discovered_ids = {exercise["id"] for exercise in exercises}
    ordered_id_set = set(ordered_ids)
    unknown_ids = sorted(ordered_id_set - discovered_ids)
    missing_ids = sorted(discovered_ids - ordered_id_set)
    if unknown_ids:
        raise RequestError(
            "exercise order contains unknown exercises: " + ", ".join(unknown_ids)
        )
    if missing_ids:
        raise RequestError(
            "exercise order is missing exercises: " + ", ".join(missing_ids)
        )
    return ordered_ids


def exercise_name(metadata: Path, fallback: str) -> str:
    """Read the first non-empty line under the metadata's Name heading."""
    lines = metadata.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.strip().casefold() != "# name":
            continue
        for candidate in lines[index + 1 :]:
            candidate = candidate.strip()
            if candidate.startswith("#"):
                break
            if candidate:
                return candidate
        break
    return fallback.replace("_", " ").title()


def collection_candidates(
    directory: str,
    source_extension: str,
    metadata_extension: str,
    store: PracticeStore,
    now: datetime,
) -> dict[str, Any]:
    path_key, collection_key, _ = collection_keys(directory)
    collection = Path(path_key)
    target_environment = load_collection_environment(collection)
    store.adopt_collection_key(path_key, collection_key)
    exercises: list[dict[str, Any]] = []
    for source in sorted(collection.glob(f"*{source_extension}")):
        if not source.is_file():
            continue
        metadata = source.with_suffix(metadata_extension)
        if metadata.is_file():
            exercises.append({
                "id": source.stem,
                "source_path": str(source.resolve()),
                "metadata_path": str(metadata.resolve()),
                "collection_directory": path_key,
                **({"target_environment": target_environment} if target_environment is not None else {}),
            })
    if not exercises:
        raise RequestError(
            f"no {source_extension}/{metadata_extension} exercise pairs found in {collection}"
        )
    order = exercise_order(collection, exercises)
    cards = store.cards_for_collection(collection_key)
    disabled_ids = store.disabled_exercise_ids(collection_key)
    by_id = {exercise["id"]: exercise for exercise in exercises}
    by_id = {exercise_id: exercise for exercise_id, exercise in by_id.items()
             if exercise_id not in disabled_ids}
    scheduled = {exercise_id: card for exercise_id, card in cards.items() if exercise_id in by_id}
    due = [(exercise_id, card) for exercise_id, card in scheduled.items() if card.due <= now]
    unseen = ([exercise_id for exercise_id in order
               if exercise_id in by_id and exercise_id not in scheduled]
              if order is not None else [exercise["id"] for exercise in exercises if exercise["id"] not in scheduled])
    return {
        "path": path_key,
        "collection_key": collection_key,
        "exercises": by_id,
        "scheduled": scheduled,
        "due": due,
        "unseen": unseen,
        "ordered_unseen": order is not None,
    }


def select_exercise(
    request: dict[str, Any], current_datetime: datetime | None = None
) -> dict[str, Any]:
    source_extension = required_string(request, "source_extension")
    metadata_extension = required_string(request, "metadata_extension")
    daily_new_limit = max_new_problems_per_day(request)
    previous_id = request.get("previous_exercise_id")
    previous = request.get("previous_exercise")
    if previous_id is not None and not isinstance(previous_id, str):
        raise RequestError("previous_exercise_id must be a string or null")
    if previous is not None and (
        not isinstance(previous, dict)
        or set(previous) != {"collection_directory", "exercise_id"}
        or not isinstance(previous["collection_directory"], str)
        or not isinstance(previous["exercise_id"], str)
    ):
        raise RequestError("previous_exercise must contain collection_directory and exercise_id strings")
    if not source_extension.startswith("."):
        raise RequestError("source_extension must start with a dot")
    if not metadata_extension.startswith("."):
        raise RequestError("metadata_extension must start with a dot")
    try:
        store = PracticeStore(database_path(request))
        now = ensure_utc(current_datetime)
        candidates = [collection_candidates(directory, source_extension, metadata_extension, store, now)
                      for directory in collection_directories(request)]
    except SchedulerError as error:
        raise RequestError(str(error)) from error
    if len({candidate["path"] for candidate in candidates}) != len(candidates):
        raise RequestError("exercise_directories must not contain duplicate paths")

    due_options = [
        (candidate, exercise_id, card)
        for candidate in candidates for exercise_id, card in candidate["due"]
    ]
    selected_candidate: dict[str, Any] | None = None
    selected_id: str | None = None
    if due_options:
        oldest_due = min(card.due for _, _, card in due_options)
        options = [(candidate, exercise_id) for candidate, exercise_id, card in due_options
                   if card.due == oldest_due]
        if previous is not None and len(options) > 1:
            options = [(candidate, exercise_id) for candidate, exercise_id in options if not (
                candidate["path"] == previous["collection_directory"]
                and exercise_id == previous["exercise_id"])] or options
        elif previous_id is not None and len(options) > 1:
            options = [(candidate, exercise_id) for candidate, exercise_id in options
                       if exercise_id != previous_id] or options
        selected_candidate, selected_id = random.SystemRandom().choice(options)
    else:
        limit_reached = (
            daily_new_limit is not None
            and introductions_today(store, [candidate["collection_key"] for candidate in candidates], now)
            >= daily_new_limit
        )
        available = ([] if limit_reached else [
            (index, candidate) for index, candidate in enumerate(candidates) if candidate["unseen"]
        ])
        if available:
            _, selected_candidate = min(
                available, key=lambda item: (len(item[1]["scheduled"]), item[0])
            )
            unseen = selected_candidate["unseen"]
            if len(unseen) > 1:
                if previous is not None and selected_candidate["path"] == previous["collection_directory"]:
                    unseen = [exercise_id for exercise_id in unseen
                              if exercise_id != previous["exercise_id"]] or unseen
                elif previous_id is not None:
                    unseen = [exercise_id for exercise_id in unseen
                              if exercise_id != previous_id] or unseen
            selected_id = (unseen[0] if selected_candidate["ordered_unseen"]
                           else random.SystemRandom().choice(unseen))
    if selected_candidate is not None and selected_id is not None:
        selected = selected_candidate["exercises"][selected_id]
        return {"exercise": {**selected, "name": exercise_name(Path(selected["metadata_path"]), selected_id)}}

    remaining_due = [
        card.due for candidate in candidates for card in candidate["scheduled"].values()
    ]
    response = {
        "exercise": None,
        "next_due": min(remaining_due).isoformat() if remaining_due else None,
    }
    if daily_new_limit is not None and not due_options and any(candidate["unseen"] for candidate in candidates):
        response["new_limit_reached"] = introductions_today(
            store, [candidate["collection_key"] for candidate in candidates], now
        ) >= daily_new_limit
        if response["new_limit_reached"]:
            next_new_available = next_new_problem_time(now)
            response["next_new_available"] = next_new_available.isoformat()
            next_due = min(remaining_due) if remaining_due else None
            response["next_available"] = min(
                candidate for candidate in (next_due, next_new_available) if candidate is not None
            ).isoformat()
    return response


def main() -> int:
    try:
        response = select_exercise(read_request())
    except (
        OSError,
        RequestError,
        SchedulerError,
        TargetEnvironmentError,
        UnicodeError,
        sqlite3.Error,
    ) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1

    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
