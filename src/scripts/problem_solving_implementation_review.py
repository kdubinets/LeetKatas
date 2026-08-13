#!/usr/bin/env python3
"""Run a bounded Level C implementation checkpoint or final review."""
from __future__ import annotations
import json, sqlite3, sys
from implementation_review_protocol import ImplementationReviewError, configured_adapter, request_review
from practice_scheduler import SchedulerError
from problem_solving_store import ProblemSolvingStore, problem_collection, problem_solving_database_path

def review(request: dict) -> dict:
    stage = request.get("stage")
    if stage not in {"checkpoint", "final"}: raise ValueError("stage must be checkpoint or final")
    draft_id = request.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id: raise ValueError("draft_id is required")
    collection, collection_key, ids = problem_collection(request.get("collection_directory"))
    store = ProblemSolvingStore(problem_solving_database_path(request)); draft = store.draft(draft_id)
    if not draft or draft["collection_key"] != collection_key or draft["problem_id"] not in ids: raise ValueError("draft not found")
    compiled = store.latest_implementation_compile(draft_id)
    if not compiled or compiled["status"] != "success" or compiled["source_hash"] != store.implementation_source_hash(draft["source"]): raise SchedulerError("a successful compile of the current draft is required before review")
    state = store.artifact(collection_key, draft["problem_id"])
    brief = (collection / "cards" / f"{draft['problem_id']}.brief.md").read_text(encoding="utf-8")
    payload = {"stage": stage, "problem": {"focused_brief": brief}, "learner_code": draft["source"]}
    if stage == "final" and state and state["revealed"]:
        teaching = json.loads((collection / "cards" / f"{draft['problem_id']}.card.json").read_text(encoding="utf-8"))["teaching"]
        payload["revealed_material"] = {"solution_outline": teaching["solution_outline"], "accepted_alternatives": teaching["accepted_alternatives"]}
    command, name = configured_adapter(request)
    result = request_review(stage, payload, command)
    store.record_implementation_review(draft_id, stage, result["status"], result["feedback"], result["failure"])
    return {**result, "stage": stage, "reviewer": name}

def main() -> int:
    try: response = review(json.load(sys.stdin))
    except (ValueError, SchedulerError, ImplementationReviewError, sqlite3.Error, json.JSONDecodeError, OSError, UnicodeError) as error:
        json.dump({"error":str(error)},sys.stdout);sys.stdout.write("\n");return 1
    json.dump(response,sys.stdout);sys.stdout.write("\n");return 0
if __name__ == "__main__": raise SystemExit(main())
