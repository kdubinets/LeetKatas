#!/usr/bin/env python3
"""Persist a practice rating and update its FSRS card."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from typing import Any

from practice_scheduler import (
    PracticeStore,
    RATING_NAMES,
    SchedulerError,
    canonical_collection,
    database_path,
)


RATINGS = RATING_NAMES


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


def record_rating(
    request: dict[str, Any], review_datetime: datetime | None = None
) -> dict[str, str | bool]:
    collection_key = canonical_collection(request.get("exercise_directory"))
    exercise_id = request.get("exercise_id")
    compiled = request.get("compiled")
    proposed_rating = request.get("proposed_rating")
    final_rating = request.get("final_rating")

    if not isinstance(exercise_id, str) or not exercise_id:
        raise RequestError("exercise_id must be a non-empty string")
    if not isinstance(compiled, bool):
        raise RequestError("compiled must be a boolean")
    if proposed_rating is not None and proposed_rating not in RATINGS:
        raise RequestError("proposed_rating must be a valid rating or null")
    if final_rating not in RATINGS:
        raise RequestError("final_rating must be a valid rating")
    try:
        return PracticeStore(database_path(request)).record_review(
            collection_key=collection_key,
            exercise_id=exercise_id,
            compiled=compiled,
            proposed_rating=proposed_rating,
            final_rating=final_rating,
            review_datetime=review_datetime,
            review_status=request.get("review_status", "available"),
            reviewer_name=request.get("reviewer_name"),
            reviewer_model=request.get("reviewer_model"),
            review_attempts=request.get("review_attempts", 0),
        )
    except SchedulerError as error:
        raise RequestError(str(error)) from error


def main() -> int:
    try:
        response = record_rating(read_request())
    except (OSError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1

    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
