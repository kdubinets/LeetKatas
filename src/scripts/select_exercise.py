#!/usr/bin/env python3
"""Select a random paired exercise from a collection directory."""

from __future__ import annotations

import json
import random
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from practice_scheduler import (
    PracticeStore,
    SchedulerError,
    canonical_collection,
    database_path,
    ensure_utc,
)


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


def select_exercise(
    request: dict[str, Any], current_datetime: datetime | None = None
) -> dict[str, Any]:
    collection_key = canonical_collection(required_string(request, "exercise_directory"))
    collection = Path(collection_key)
    source_extension = required_string(request, "source_extension")
    metadata_extension = required_string(request, "metadata_extension")
    previous_id = request.get("previous_exercise_id")

    if previous_id is not None and not isinstance(previous_id, str):
        raise RequestError("previous_exercise_id must be a string or null")
    if not source_extension.startswith("."):
        raise RequestError("source_extension must start with a dot")
    if not metadata_extension.startswith("."):
        raise RequestError("metadata_extension must start with a dot")
    exercises: list[dict[str, str]] = []
    for source in sorted(collection.glob(f"*{source_extension}")):
        if not source.is_file():
            continue
        metadata = source.with_suffix(metadata_extension)
        if metadata.is_file():
            exercises.append(
                {
                    "id": source.stem,
                    "source_path": str(source.resolve()),
                    "metadata_path": str(metadata.resolve()),
                }
            )

    if not exercises:
        raise RequestError(
            f"no {source_extension}/{metadata_extension} exercise pairs found in {collection}"
        )

    try:
        cards = PracticeStore(database_path(request)).cards_for_collection(collection_key)
        now = ensure_utc(current_datetime)
    except SchedulerError as error:
        raise RequestError(str(error)) from error

    exercise_by_id = {exercise["id"]: exercise for exercise in exercises}
    scheduled = {
        exercise_id: card
        for exercise_id, card in cards.items()
        if exercise_id in exercise_by_id
    }
    due = [(exercise_id, card) for exercise_id, card in scheduled.items() if card.due <= now]
    if due:
        oldest_due = min(card.due for _, card in due)
        candidate_ids = [exercise_id for exercise_id, card in due if card.due == oldest_due]
    else:
        candidate_ids = [
            exercise["id"]
            for exercise in exercises
            if exercise["id"] not in scheduled
        ]

    if candidate_ids:
        if len(candidate_ids) > 1 and previous_id in candidate_ids:
            candidate_ids = [
                exercise_id for exercise_id in candidate_ids if exercise_id != previous_id
            ]
        selected_id = random.SystemRandom().choice(candidate_ids)
        return {"exercise": exercise_by_id[selected_id]}

    next_due = min(card.due for card in scheduled.values())
    return {"exercise": None, "next_due": next_due.isoformat()}


def main() -> int:
    try:
        response = select_exercise(read_request())
    except (OSError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1

    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
