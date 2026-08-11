"""Strict schemas and retry handling for Level C conversation adapters."""

from __future__ import annotations

import json
import os
import subprocess
import time
from typing import Any


class ConversationError(ValueError):
    pass


def validate_history(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) > 16:
        raise ConversationError("history must be an array of at most 16 messages")
    result: list[dict[str, str]] = []
    expected = "user"
    total = 0
    for index, message in enumerate(value):
        if not isinstance(message, dict) or set(message) != {"role", "content"}:
            raise ConversationError(f"history[{index}] must contain only role and content")
        role = message.get("role")
        content = message.get("content")
        if role != expected:
            raise ConversationError("history messages must alternate user and assistant roles")
        if not isinstance(content, str) or not content.strip():
            raise ConversationError(f"history[{index}].content must be a non-empty string")
        total += len(content)
        result.append({"role": role, "content": content.strip()})
        expected = "assistant" if expected == "user" else "user"
    if expected == "assistant":
        raise ConversationError("history must contain complete user/assistant turns")
    if total > 65536:
        raise ConversationError("history must be at most 65536 characters")
    return result


def validate_question(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConversationError("question must be a non-empty string")
    question = value.strip()
    if len(question) > 8000:
        raise ConversationError("question must be at most 8000 characters")
    return question


def _string_array(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ConversationError(f"{context} must be an array of non-empty strings")
    return [item.strip() for item in value]


def validate_clarification_response(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"status", "answer", "disclosure"}:
        raise ConversationError(
            "clarification response must contain only status, answer, and disclosure"
        )
    status = value.get("status")
    disclosure = value.get("disclosure")
    if status not in {"answered", "redirected"}:
        raise ConversationError("clarification response.status is invalid")
    if status == "answered" and disclosure != "clarification":
        raise ConversationError("answered clarification must declare clarification disclosure")
    if status == "redirected" and disclosure != "none":
        raise ConversationError("redirected clarification must declare no disclosure")
    answer = value.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ConversationError("clarification response.answer must be a non-empty string")
    return {"status": status, "answer": answer.strip(), "disclosure": disclosure}


def validate_discussion_response(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "status", "answer", "references", "follow_up_suggestions"
    }:
        raise ConversationError(
            "discussion response must contain only status, answer, references, and follow_up_suggestions"
        )
    if value.get("status") != "answered":
        raise ConversationError("discussion response.status must be answered")
    answer = value.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ConversationError("discussion response.answer must be a non-empty string")
    return {
        "status": "answered",
        "answer": answer.strip(),
        "references": _string_array(value.get("references"), "discussion response.references"),
        "follow_up_suggestions": _string_array(
            value.get("follow_up_suggestions"),
            "discussion response.follow_up_suggestions",
        ),
    }


def configured_conversation_adapter(
    request: dict[str, Any],
) -> tuple[list[str] | None, str, str | None, str | None]:
    config = request.get("reviewer")
    if config is None:
        return None, "none", None, None
    if not isinstance(config, dict):
        raise ConversationError("reviewer must be an object")
    command = config.get("command")
    if not isinstance(command, list) or not command or any(
        not isinstance(item, str) or not item for item in command
    ):
        raise ConversationError("reviewer.command must be a non-empty array")
    name = config.get("name", os.path.basename(command[0]))
    model = config.get("model")
    effort = config.get("reasoning_effort")
    if not isinstance(name, str) or not name:
        raise ConversationError("reviewer.name must be a non-empty string")
    if model is not None and (not isinstance(model, str) or not model):
        raise ConversationError("reviewer.model must be a non-empty string or null")
    if effort is not None and (not isinstance(effort, str) or not effort):
        raise ConversationError("reviewer.reasoning_effort must be a non-empty string or null")
    return command, name, model, effort


def conversation_request(
    mode: str,
    payload: dict[str, Any],
    command: list[str] | None,
    timeout: float = 60,
) -> dict[str, Any]:
    if mode not in {"clarification", "discussion"}:
        raise ConversationError("conversation mode is invalid")
    if command is None:
        return {
            "status": "unavailable",
            "attempts": 0,
            "response": None,
            "failure": "reviewer_not_configured",
        }
    validator = (
        validate_clarification_response
        if mode == "clarification"
        else validate_discussion_response
    )
    failure = "reviewer_failed"
    for attempt in range(1, 4):
        try:
            result = subprocess.run(
                command,
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            if result.returncode != 0:
                failure = "reviewer_exited_unsuccessfully"
                raise ConversationError(failure)
            try:
                decoded = json.loads(result.stdout)
            except json.JSONDecodeError as error:
                failure = "malformed_reviewer_json"
                raise ConversationError(failure) from error
            return {
                "status": "available",
                "attempts": attempt,
                "response": validator(decoded),
                "failure": None,
            }
        except FileNotFoundError:
            return {
                "status": "unavailable",
                "attempts": attempt,
                "response": None,
                "failure": "reviewer_executable_unavailable",
            }
        except subprocess.TimeoutExpired:
            failure = "reviewer_timed_out"
        except ConversationError as error:
            failure = str(error)
        if attempt < 3:
            time.sleep(0.5 * (2 ** (attempt - 1)))
    return {
        "status": "unavailable",
        "attempts": 3,
        "response": None,
        "failure": failure,
    }
