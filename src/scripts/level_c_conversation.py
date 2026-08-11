"""Collection-aware Level C clarification and discussion orchestration."""

from __future__ import annotations

import json
from typing import Any

from level_c_conversation_protocol import (
    ConversationError,
    configured_conversation_adapter,
    conversation_request,
    validate_history,
    validate_question,
)
from practice_scheduler import SchedulerError
from problem_solving_store import (
    ProblemSolvingStore,
    problem_collection,
    problem_solving_database_path,
)


def _context(request: dict[str, Any]) -> tuple[Any, str, str, ProblemSolvingStore, dict[str, Any]]:
    collection, collection_key, problem_ids = problem_collection(
        request.get("collection_directory")
    )
    problem_id = request.get("problem_id")
    if problem_id not in problem_ids:
        raise ConversationError("problem_id is not in the collection")
    store = ProblemSolvingStore(problem_solving_database_path(request))
    state = store.artifact(collection_key, problem_id)
    if state is None:
        state = store.update_artifact(collection_key, problem_id)
    return collection, collection_key, problem_id, store, state


def _retention(request: dict[str, Any]) -> bool:
    value = request.get("retain_conversation_history", True)
    if not isinstance(value, bool):
        raise ConversationError("retain_conversation_history must be a boolean")
    return value


def _history(request: dict[str, Any], state: dict[str, Any], retain: bool) -> list[dict[str, str]]:
    value = state["conversation_history"] if retain else request.get("history", [])
    return validate_history(value)


def _reviewer_result(request: dict[str, Any], mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    command, name, model, effort = configured_conversation_adapter(request)
    result = conversation_request(mode, payload, command)
    return {
        **result,
        "reviewer": name,
        "model": model,
        "reasoning_effort": effort,
    }


def _append_turn(
    history: list[dict[str, str]], question: str, answer: str
) -> list[dict[str, str]]:
    return validate_history(
        [
            *history[-14:],
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    )


def clarify(request: dict[str, Any]) -> dict[str, Any]:
    collection, collection_key, problem_id, store, state = _context(request)
    if state["revealed"]:
        raise SchedulerError("clarification is available only before reveal")
    question = validate_question(request.get("question"))
    retain = _retention(request)
    history = _history(request, state, retain)
    brief = (collection / "cards" / f"{problem_id}.brief.md").read_text(encoding="utf-8")
    result = _reviewer_result(
        request,
        "clarification",
        {
            "problem": {
                "focused_brief": brief,
                "optional_hint_requested": state["hint_requested"],
            },
            "question": question,
            "history": history,
        },
    )
    response = result.pop("response")
    if response is None:
        store.update_artifact(collection_key, problem_id, clarification_used=True)
        return {
            **result,
            "answer": None,
            "disclosure": "none",
            "conversation_history": history,
        }
    updated_history = _append_turn(history, question, response["answer"])
    store.update_artifact(
        collection_key,
        problem_id,
        clarification_used=True,
        conversation_history=updated_history if retain else None,
    )
    return {
        **result,
        **response,
        "conversation_history": updated_history,
    }


def discuss(request: dict[str, Any]) -> dict[str, Any]:
    collection, collection_key, problem_id, store, state = _context(request)
    if not state["revealed"]:
        raise SchedulerError("discussion is available only after reveal")
    question = validate_question(request.get("question"))
    retain = _retention(request)
    history = _history(request, state, retain)
    brief = (collection / "cards" / f"{problem_id}.brief.md").read_text(encoding="utf-8")
    card = json.loads(
        (collection / "cards" / f"{problem_id}.card.json").read_text(encoding="utf-8")
    )
    teaching = card["teaching"]
    result = _reviewer_result(
        request,
        "discussion",
        {
            "problem": {
                "focused_brief": brief,
                "optional_hint": teaching["hint"],
                "solution_outline": teaching["solution_outline"],
                "accepted_alternatives": teaching["accepted_alternatives"],
            },
            "learner_context": {"hint_requested": state["hint_requested"]},
            "history": history,
            "question": question,
        },
    )
    response = result.pop("response")
    if response is None:
        return {**result, "answer": None, "references": [],
                "follow_up_suggestions": [], "conversation_history": history}
    updated_history = _append_turn(history, question, response["answer"])
    if retain:
        store.update_artifact(
            collection_key, problem_id, conversation_history=updated_history
        )
    return {**result, **response, "conversation_history": updated_history}
