#!/usr/bin/env python3
"""Record a learner-authored Level C rating after outline reveal."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from typing import Any

from practice_scheduler import RATING_NAMES, SchedulerError
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def record_problem_rating(
    request: dict[str, Any], review_datetime: datetime | None = None
) -> dict[str, Any]:
    _, collection_key, ordered_ids = problem_collection(request.get("collection_directory"))
    problem_id = request.get("problem_id")
    if problem_id not in ordered_ids:
        raise RequestError("problem_id is not in the collection")
    rating = request.get("final_rating")
    if rating not in RATING_NAMES:
        raise RequestError("final_rating must be a valid rating")
    durations: list[int] = []
    for name in ("solve_duration_ms", "discussion_duration_ms"):
        value = request.get(name)
        if type(value) is not int or value < 0:
            raise RequestError(f"{name} must be a non-negative integer")
        durations.append(value)
    store = ProblemSolvingStore(problem_solving_database_path(request))
    return store.record_review(
        collection_key,
        problem_id,
        rating,
        durations[0],
        durations[1],
        review_datetime,
    )


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = record_problem_rating(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
