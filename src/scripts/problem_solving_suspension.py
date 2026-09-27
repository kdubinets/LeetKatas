#!/usr/bin/env python3
"""Suspend, restore, or list Level C problems."""

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


def suspension_action(
    request: dict[str, Any], event_datetime: datetime | None = None
) -> dict[str, Any]:
    collection, collection_key, ordered_ids = problem_collection(request.get("collection_directory"))
    action = request.get("action")
    if action not in {"list", "suspend", "restore"}:
        raise RequestError("action must be list, suspend, or restore")
    store = ProblemSolvingStore(problem_solving_database_path(request))
    if action == "list":
        suspended = store.suspensions(collection_key)
        return {"suspended": [
            {"problem_id": problem_id,
             "title": (collection / "cards" / f"{problem_id}.brief.md").read_text(encoding="utf-8").splitlines()[0].removeprefix("# "),
             "brief_path": str(collection / "cards" / f"{problem_id}.brief.md"),
             "suspended_at": suspended[problem_id]["event_datetime"]}
            for problem_id in ordered_ids if problem_id in suspended
        ]}
    problem_id = request.get("problem_id")
    if problem_id not in ordered_ids:
        raise RequestError("problem_id is not in the collection")
    return store.update_suspension(collection_key, problem_id, action, event_datetime)


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = suspension_action(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
