#!/usr/bin/env python3
"""JSON entry point for Level C implementation draft lifecycle."""
from __future__ import annotations
import json, sqlite3, sys
from typing import Any
from practice_scheduler import SchedulerError
from problem_solving_store import ProblemSolvingStore, problem_collection, problem_solving_database_path

class RequestError(ValueError): pass

def header(brief: str) -> str:
    return "/*\n" + "\n".join(" * " + line for line in brief.strip().splitlines()) + "\n */\n\n"

def action(request: dict[str, Any]) -> dict[str, Any]:
    collection, collection_key, ids = problem_collection(request.get("collection_directory"))
    verb = request.get("action", "get")
    language = request.get("language", "cpp")
    if language != "cpp": raise RequestError("language must be cpp")
    store = ProblemSolvingStore(problem_solving_database_path(request))
    if verb == "list": return {"drafts": store.list_current_drafts(collection_key)}
    draft_id = request.get("draft_id")
    if verb in {"get", "save"}:
        if not isinstance(draft_id, str) or not draft_id: raise RequestError("draft_id is required")
        draft = store.draft(draft_id)
        if not draft or draft["collection_key"] != collection_key: raise RequestError("draft not found")
        if verb == "save": draft = store.save_draft_source(draft_id, request.get("source"))
        return {"draft": draft}
    problem_id = request.get("problem_id")
    if problem_id not in ids: raise RequestError("problem_id is not in the collection")
    if verb not in {"open", "fresh"}: raise RequestError("action must be list, get, save, open, or fresh")
    brief = (collection / "cards" / f"{problem_id}.brief.md").read_text(encoding="utf-8")
    draft = store.create_or_resume_draft(collection_key, problem_id, header(brief), language, fresh=verb == "fresh")
    return {"draft": draft, "resumed": verb == "open" and draft["source"] != header(brief)}

def main() -> int:
    try:
        value = json.load(sys.stdin)
        if not isinstance(value, dict): raise RequestError("request must be a JSON object")
        response = action(value)
    except (RequestError, SchedulerError, sqlite3.Error, OSError, UnicodeError, json.JSONDecodeError) as error:
        json.dump({"error": str(error)}, sys.stdout); sys.stdout.write("\n"); return 1
    json.dump(response, sys.stdout); sys.stdout.write("\n"); return 0
if __name__ == "__main__": raise SystemExit(main())
