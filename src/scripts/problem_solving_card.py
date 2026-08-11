#!/usr/bin/env python3
"""Read a Level C card through its hint/reveal visibility boundary."""

from __future__ import annotations

import json
import sqlite3
import sys
from typing import Any

from practice_scheduler import SchedulerError
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


class RequestError(ValueError):
    pass


def card_action(request: dict[str, Any]) -> dict[str, Any]:
    collection, collection_key, ordered_ids = problem_collection(
        request.get("collection_directory")
    )
    problem_id = request.get("problem_id")
    if problem_id not in ordered_ids:
        raise RequestError("problem_id is not in the collection")
    action = request.get("action", "get")
    if action not in {"get", "hint", "clarification", "reveal"}:
        raise RequestError("action must be get, hint, clarification, or reveal")
    record_path = collection / "cards" / f"{problem_id}.card.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    brief_path = (collection / "cards" / f"{problem_id}.brief.md").resolve()
    store = ProblemSolvingStore(problem_solving_database_path(request))
    if action == "hint":
        state = store.update_artifact(collection_key, problem_id, hint_requested=True)
    elif action == "clarification":
        state = store.update_artifact(collection_key, problem_id, clarification_used=True)
    elif action == "reveal":
        gave_up = request.get("gave_up", False)
        if not isinstance(gave_up, bool):
            raise RequestError("gave_up must be a boolean")
        state = store.update_artifact(
            collection_key, problem_id, revealed=True, gave_up=gave_up
        )
    else:
        state = store.artifact(collection_key, problem_id) or {
            "hint_requested": False,
            "clarification_used": False,
            "revealed": False,
            "gave_up": False,
            "selected_at": None,
            "revealed_at": None,
            "note": None,
            "conversation_history": [],
        }
    response: dict[str, Any] = {
        "problem_id": problem_id,
        "brief_path": str(brief_path),
        "state": state,
    }
    if state["hint_requested"]:
        response["hint"] = record["teaching"]["hint"]
    if state["revealed"]:
        response["solution_outline"] = record["teaching"]["solution_outline"]
        response["accepted_alternatives"] = record["teaching"]["accepted_alternatives"]
    return response


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RequestError("request must be a JSON object")
        response = card_action(request)
    except (json.JSONDecodeError, OSError, UnicodeError, RequestError, SchedulerError, sqlite3.Error) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
