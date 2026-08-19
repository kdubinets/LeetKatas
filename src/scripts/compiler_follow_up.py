#!/usr/bin/env python3
"""Ask the configured LLM to explain compiler output without grading work."""
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
        raise RequestError("request must be an object")
    return value


def ask(request: dict[str, Any]) -> dict[str, Any]:
    question, evidence = request.get("question"), request.get("evidence")
    messages = request.get("messages", [])
    if not isinstance(question, str) or not question.strip() or len(question) > 8000:
        raise RequestError("question must be a non-empty string of at most 8000 characters")
    if not isinstance(evidence, dict):
        raise RequestError("evidence must be an object")
    if not isinstance(messages, list) or len(messages) > 16:
        raise RequestError("messages must be an array of at most 16 items")
    if any(not isinstance(item, dict) or item.get("role") not in {"user", "assistant"}
           or not isinstance(item.get("content"), str) for item in messages):
        raise RequestError("each message must have a valid role and string content")
    command, name = configured_reviewer(request)
    config = request.get("reviewer")
    response = follow_up_request({"evidence": evidence, "messages": messages,
                                  "question": question.strip()}, command) if command else {
        "status": "unavailable", "attempts": 0, "answer": None,
        "failure": "no compiler-question reviewer configured"}
    return {**response, "reviewer": name,
            "model": config.get("model") if isinstance(config, dict) else None,
            "reasoning_effort": config.get("reasoning_effort") if isinstance(config, dict) else None}


def main() -> int:
    try:
        response = ask(read_request())
    except (RequestError, ReviewerError) as error:
        json.dump({"error": str(error)}, sys.stdout); sys.stdout.write("\n"); return 1
    json.dump(response, sys.stdout); sys.stdout.write("\n"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
