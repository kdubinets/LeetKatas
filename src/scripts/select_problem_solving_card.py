#!/usr/bin/env python3
"""Select a due or canonically unseen Level C problem card."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from typing import Any

from practice_scheduler import SchedulerError, ensure_utc
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def select_problem(
    request: dict[str, Any], current_datetime: datetime | None = None
) -> dict[str, Any]:
    collection, collection_key, ordered_ids = problem_collection(
        request.get("collection_directory")
    )
    previous_id = request.get("previous_problem_id")
    if previous_id is not None and not isinstance(previous_id, str):
        raise RequestError("previous_problem_id must be a string or null")
    now = ensure_utc(current_datetime)
    store = ProblemSolvingStore(problem_solving_database_path(request))
    cards = store.cards_for_collection(collection_key)
    bookmarked = store.open_bookmark_ids(collection_key)
    active_ids = [problem_id for problem_id in ordered_ids if problem_id not in bookmarked]
    due_ids = [
        problem_id
        for problem_id in active_ids
        if problem_id in cards and cards[problem_id].due <= now
    ]
    if due_ids:
        oldest = min(cards[problem_id].due for problem_id in due_ids)
        candidates = [problem_id for problem_id in due_ids if cards[problem_id].due == oldest]
    else:
        candidates = [problem_id for problem_id in active_ids if problem_id not in cards]
    if len(candidates) > 1 and previous_id in candidates:
        candidates = [problem_id for problem_id in candidates if problem_id != previous_id]
    if not candidates:
        future = [cards[problem_id].due for problem_id in active_ids if problem_id in cards]
        return {
            "problem": None,
            "next_due": min(future).isoformat() if future else None,
            "open_bookmarks": len(bookmarked),
        }
    selected = candidates[0]
    brief_path = (collection / "cards" / f"{selected}.brief.md").resolve()
    title = brief_path.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
    artifact = store.artifact(collection_key, selected)
    if artifact is None:
        artifact = store.update_artifact(
            collection_key, selected, updated_at=now
        )
    return {
        "problem": {
            "id": selected,
            "title": title,
            "brief_path": str(brief_path),
            "state": artifact,
        },
        "next_due": None,
        "open_bookmarks": len(bookmarked),
    }


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = select_problem(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
