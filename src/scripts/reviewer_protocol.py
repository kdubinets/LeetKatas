"""Protocol and retry support for external practice reviewers."""
from __future__ import annotations
import json, os, subprocess, time
from typing import Any, Callable

VERDICTS = {"correct", "minor_defect", "incorrect", "cannot_assess"}
RATINGS = {"fail", "acceptable", "good", "excellent"}

class ReviewerError(ValueError): pass

def validate_review(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict): raise ReviewerError("review must be an object")
    for key in ("verdict", "summary", "correctness_analysis", "code_quality_analysis", "rating_explanation"):
        if not isinstance(value.get(key), str): raise ReviewerError(f"review.{key} must be a string")
    if value["verdict"] not in VERDICTS: raise ReviewerError("invalid review verdict")
    rating = value.get("proposed_rating")
    if rating is not None and rating not in RATINGS: raise ReviewerError("invalid proposed rating")
    for key in ("major_issues", "minor_issues"):
        if not isinstance(value.get(key), list) or any(not isinstance(x, str) for x in value[key]):
            raise ReviewerError(f"review.{key} must be an array of strings")
    for key in (
        "improved_implementation",
        "improvement_explanation",
        "alternative_implementation",
        "alternative_explanation",
        "version_notes",
    ):
        if key in value and value[key] is not None and not isinstance(value[key], str): raise ReviewerError(f"review.{key} must be a string or null")
    return value

def validate_follow_up(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ReviewerError("follow-up response must be an object")
    answer = value.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ReviewerError("follow-up response.answer must be a non-empty string")
    return {"answer": answer.strip()}

def review_request(
    request: dict[str, Any],
    command: list[str],
    timeout: float = 60,
    progress: Callable[..., None] | None = None,
) -> dict[str, Any]:
    last = "reviewer failed"
    for attempt in range(1, 4):
        if progress:
            progress("review_attempt_started", attempt=attempt, maximum_attempts=3)
        try:
            result = subprocess.run(command, input=json.dumps(request), text=True, capture_output=True, timeout=timeout, check=False)
            if result.returncode != 0: raise ReviewerError((result.stderr or result.stdout or "reviewer exited unsuccessfully").strip())
            try: value = json.loads(result.stdout)
            except json.JSONDecodeError as error: raise ReviewerError(f"malformed reviewer JSON: {error.msg}") from error
            review = validate_review(value)
            if progress:
                progress("review_finished", status="available", attempts=attempt)
            return {"status": "available", "attempts": attempt, "feedback": review, "failure": None}
        except FileNotFoundError:
            if progress:
                progress("review_finished", status="unavailable", attempts=attempt)
            return {"status": "unavailable", "attempts": attempt, "feedback": None, "failure": f"reviewer executable is not available: {command[0]}"}
        except ReviewerError as error:
            last = str(error)
        except subprocess.TimeoutExpired: last = f"reviewer timed out after {timeout:g} seconds"
        if progress:
            progress("review_attempt_failed", attempt=attempt)
        if attempt < 3:
            delay = 0.5 * (2 ** (attempt - 1))
            if progress:
                progress("review_retry_scheduled", next_attempt=attempt + 1, delay_seconds=delay)
            time.sleep(delay)
    if progress:
        progress("review_finished", status="unavailable", attempts=3)
    return {"status": "unavailable", "attempts": 3, "feedback": None, "failure": last}

def follow_up_request(
    request: dict[str, Any],
    command: list[str],
    timeout: float = 60,
) -> dict[str, Any]:
    last = "follow-up reviewer failed"
    for attempt in range(1, 4):
        try:
            result = subprocess.run(
                command,
                input=json.dumps(request),
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            if result.returncode != 0:
                raise ReviewerError(
                    (result.stderr or result.stdout or "follow-up reviewer exited unsuccessfully").strip()
                )
            try:
                value = json.loads(result.stdout)
            except json.JSONDecodeError as error:
                raise ReviewerError(f"malformed follow-up reviewer JSON: {error.msg}") from error
            response = validate_follow_up(value)
            return {
                "status": "available",
                "attempts": attempt,
                "answer": response["answer"],
                "failure": None,
            }
        except FileNotFoundError:
            return {
                "status": "unavailable",
                "attempts": attempt,
                "answer": None,
                "failure": f"follow-up reviewer executable is not available: {command[0]}",
            }
        except ReviewerError as error:
            last = str(error)
        except subprocess.TimeoutExpired:
            last = f"follow-up reviewer timed out after {timeout:g} seconds"
        if attempt < 3:
            time.sleep(0.5 * (2 ** (attempt - 1)))
    return {"status": "unavailable", "attempts": 3, "answer": None, "failure": last}

def configured_reviewer(request: dict[str, Any]) -> tuple[list[str] | None, str]:
    config = request.get("reviewer")
    if config is None: return None, "none"
    command = config.get("command") if isinstance(config, dict) else config
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x for x in command): raise ReviewerError("reviewer.command must be a non-empty array")
    return command, str(config.get("name", os.path.basename(command[0])) if isinstance(config, dict) else os.path.basename(command[0]))
