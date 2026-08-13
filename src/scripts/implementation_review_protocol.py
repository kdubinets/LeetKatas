"""Strict, visibility-safe contracts for Level C implementation reviews."""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any


class ImplementationReviewError(ValueError):
    pass


def _text(value: Any, field: str, maximum: int = 4000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > maximum:
        raise ImplementationReviewError(f"{field} must be a non-empty string of at most {maximum} characters")
    return value.strip()


def validate_response(stage: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict): raise ImplementationReviewError("review response must be an object")
    if stage == "checkpoint":
        if set(value) != {"status", "feedback"} or value.get("status") not in {"likely_sound", "concern"}:
            raise ImplementationReviewError("checkpoint response must contain status and feedback")
        return {"status": value["status"], "feedback": _text(value["feedback"], "checkpoint feedback", 1200)}
    if stage == "final":
        if set(value) != {"status", "sound", "issues", "interview_communication"} or value.get("status") != "reviewed":
            raise ImplementationReviewError("final response has an invalid shape")
        if not isinstance(value["issues"], list) or len(value["issues"]) > 8:
            raise ImplementationReviewError("final issues must be an array of at most eight items")
        return {"status": "reviewed", "sound": _text(value["sound"], "final sound", 2400), "issues": [_text(x, "final issue", 1200) for x in value["issues"]], "interview_communication": _text(value["interview_communication"], "interview communication", 1200)}
    raise ImplementationReviewError("review stage must be checkpoint or final")


def configured_adapter(request: dict[str, Any]) -> tuple[list[str] | None, str]:
    reviewer = request.get("reviewer")
    if reviewer is None: return None, "none"
    if not isinstance(reviewer, dict) or not isinstance(reviewer.get("command"), list) or not reviewer["command"] or any(not isinstance(x, str) or not x for x in reviewer["command"]):
        raise ImplementationReviewError("reviewer.command must be a non-empty array")
    return reviewer["command"], reviewer.get("name", os.path.basename(reviewer["command"][0]))


def request_review(stage: str, payload: dict[str, Any], command: list[str] | None) -> dict[str, Any]:
    if command is None: return {"status": "unavailable", "attempts": 0, "feedback": None, "failure": "reviewer_not_configured"}
    try:
        result = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True, timeout=60, check=False)
        if result.returncode: raise ImplementationReviewError("reviewer_exited_unsuccessfully")
        return {"status": "available", "attempts": 1, "feedback": validate_response(stage, json.loads(result.stdout)), "failure": None}
    except FileNotFoundError:
        return {"status": "unavailable", "attempts": 1, "feedback": None, "failure": "reviewer_executable_unavailable"}
    except subprocess.TimeoutExpired:
        return {"status": "unavailable", "attempts": 1, "feedback": None, "failure": "reviewer_timed_out"}
    except (json.JSONDecodeError, ImplementationReviewError) as error:
        return {"status": "unavailable", "attempts": 1, "feedback": None, "failure": str(error)}
