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
    submitted_source = request.get("submitted_source")
    review_response = request.get("review_response")
    review_archive_ttl_days = request.get("review_archive_ttl_days", 30)

    if not isinstance(exercise_id, str) or not exercise_id:
        raise RequestError("exercise_id must be a non-empty string")
    if not isinstance(compiled, bool):
        raise RequestError("compiled must be a boolean")
    if proposed_rating is not None and proposed_rating not in RATINGS:
        raise RequestError("proposed_rating must be a valid rating or null")
    if final_rating not in RATINGS:
        raise RequestError("final_rating must be a valid rating")
    if type(review_archive_ttl_days) is not int or not 0 <= review_archive_ttl_days <= 3650:
        raise RequestError("review_archive_ttl_days must be an integer between 0 and 3650")
    if submitted_source is not None and not isinstance(submitted_source, str):
        raise RequestError("submitted_source must be a string or null")
    if review_response is not None and not isinstance(review_response, dict):
        raise RequestError("review_response must be an object or null")
    if (submitted_source is None) != (review_response is None):
        raise RequestError("submitted_source and review_response must be provided together")
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
            reviewer_reasoning_effort=request.get("reviewer_reasoning_effort"),
            review_attempts=request.get("review_attempts", 0),
            submitted_source=submitted_source,
            review_response=review_response,
            review_archive_ttl_days=review_archive_ttl_days,
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
