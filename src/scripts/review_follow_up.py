#!/usr/bin/env python3
"""Ask a configured reviewer a conversational question about a completed review."""
from __future__ import annotations

import json
import sys
from typing import Any

from reviewer_protocol import ReviewerError, configured_reviewer, follow_up_request


class RequestError(ValueError):
    pass


def read_request() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise RequestError(f"invalid JSON request: {error.msg}") from error
    if not isinstance(value, dict):
        raise RequestError("request must be a JSON object")
    return value


def ask(request: dict[str, Any]) -> dict[str, Any]:
    question = request.get("question")
    if not isinstance(question, str) or not question.strip():
        raise RequestError("question must be a non-empty string")
    if len(question) > 8000:
        raise RequestError("question must be at most 8000 characters")
    evidence = request.get("evidence")
    initial_review = request.get("initial_review")
    messages = request.get("messages", [])
    if not isinstance(evidence, dict):
        raise RequestError("evidence must be an object")
    if not isinstance(initial_review, dict):
        raise RequestError("initial_review must be an object")
    if not isinstance(messages, list) or len(messages) > 16:
        raise RequestError("messages must be an array of at most 16 items")
    for message in messages:
        if (
            not isinstance(message, dict)
            or message.get("role") not in {"user", "assistant"}
            or not isinstance(message.get("content"), str)
        ):
            raise RequestError("each message must have a valid role and string content")
    if sum(len(message["content"]) for message in messages) > 65536:
        raise RequestError("conversation history must be at most 65536 characters")

    command, name = configured_reviewer(request)
    reviewer_config = request.get("reviewer")
    model = reviewer_config.get("model") if isinstance(reviewer_config, dict) else None
    effort = reviewer_config.get("reasoning_effort") if isinstance(reviewer_config, dict) else None
    if command:
        response = follow_up_request(
            {
                "evidence": evidence,
                "initial_review": initial_review,
                "messages": messages,
                "question": question.strip(),
            },
            command,
        )
    else:
        response = {
            "status": "unavailable",
            "attempts": 0,
            "answer": None,
            "failure": "no follow-up reviewer configured",
        }
    return {
        **response,
        "reviewer": name,
        "model": model if isinstance(model, str) else None,
        "reasoning_effort": effort if isinstance(effort, str) else None,
    }


def main() -> int:
    try:
        response = ask(read_request())
    except (RequestError, ReviewerError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
