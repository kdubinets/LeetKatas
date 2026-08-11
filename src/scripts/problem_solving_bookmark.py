#!/usr/bin/env python3
"""Create, update, list, or remove Level C open-thinking bookmarks."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from typing import Any

from practice_scheduler import SchedulerError
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def bookmark_action(
    request: dict[str, Any], event_datetime: datetime | None = None
) -> dict[str, Any]:
    _, collection_key, ordered_ids = problem_collection(request.get("collection_directory"))
    action = request.get("action")
    if action not in {"list", "create", "update", "remove"}:
        raise RequestError("action must be list, create, update, or remove")
    store = ProblemSolvingStore(problem_solving_database_path(request))
    if action == "list":
        return {"bookmarks": store.list_bookmarks(collection_key)}
    problem_id = request.get("problem_id")
    if problem_id not in ordered_ids:
        raise RequestError("problem_id is not in the collection")
    note = request.get("note", ...)
    if note is not ... and note is not None and not isinstance(note, str):
        raise RequestError("note must be a string or null")
    result = store.update_bookmark(
        collection_key, problem_id, action, note=note, event_datetime=event_datetime
    )
    return result


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = bookmark_action(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
