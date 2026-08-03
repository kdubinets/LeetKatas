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
    collection_keys,
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
    path_key, collection_key, _ = collection_keys(request.get("exercise_directory"))
    exercise_id = request.get("exercise_id")
    compiled = request.get("compiled")
    proposed_rating = request.get("proposed_rating")
    final_rating = request.get("final_rating")
    submitted_source = request.get("submitted_source")
    review_response = request.get("review_response")
    review_archive_ttl_days = request.get("review_archive_ttl_days", 30)
    solve_duration_ms = request.get("solve_duration_ms")
    feedback_duration_ms = request.get("feedback_duration_ms")

    if not isinstance(exercise_id, str) or not exercise_id or len(exercise_id) > 512:
        raise RequestError("exercise_id must be a non-empty string")
    if not isinstance(compiled, bool):
        raise RequestError("compiled must be a boolean")
    if proposed_rating is not None and proposed_rating not in RATINGS:
        raise RequestError("proposed_rating must be a valid rating or null")
    if final_rating not in RATINGS:
        raise RequestError("final_rating must be a valid rating")
    review_status = request.get("review_status", "available")
    review_attempts = request.get("review_attempts", 0)
    if not isinstance(review_status, str) or not review_status or len(review_status) > 512:
        raise RequestError("review_status must be a non-empty string")
    if type(review_attempts) is not int or review_attempts < 0:
        raise RequestError("review_attempts must be a non-negative integer")
    for name in ("reviewer_name", "reviewer_model", "reviewer_reasoning_effort"):
        value = request.get(name)
        if value is not None and (
            not isinstance(value, str) or not value or len(value) > 512
        ):
            raise RequestError(f"{name} must be a non-empty string or null")
    if type(review_archive_ttl_days) is not int or not 0 <= review_archive_ttl_days <= 3650:
        raise RequestError("review_archive_ttl_days must be an integer between 0 and 3650")
    if submitted_source is not None and not isinstance(submitted_source, str):
        raise RequestError("submitted_source must be a string or null")
    if review_response is not None and not isinstance(review_response, dict):
        raise RequestError("review_response must be an object or null")
    if (submitted_source is None) != (review_response is None):
        raise RequestError("submitted_source and review_response must be provided together")
    for name, value in (
        ("solve_duration_ms", solve_duration_ms),
        ("feedback_duration_ms", feedback_duration_ms),
    ):
        if value is not None and (type(value) is not int or value < 0):
            raise RequestError(f"{name} must be a non-negative integer or null")
    if (solve_duration_ms is None) != (feedback_duration_ms is None):
        raise RequestError("solve_duration_ms and feedback_duration_ms must be provided together")
    try:
        store = PracticeStore(database_path(request))
        store.adopt_collection_key(path_key, collection_key)
        return store.record_review(
            collection_key=collection_key,
            exercise_id=exercise_id,
            compiled=compiled,
            proposed_rating=proposed_rating,
            final_rating=final_rating,
            review_datetime=review_datetime,
            review_status=review_status,
            reviewer_name=request.get("reviewer_name"),
            reviewer_model=request.get("reviewer_model"),
            reviewer_reasoning_effort=request.get("reviewer_reasoning_effort"),
            review_attempts=review_attempts,
            solve_duration_ms=solve_duration_ms,
            feedback_duration_ms=feedback_duration_ms,
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
