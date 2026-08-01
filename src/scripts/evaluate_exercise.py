#!/usr/bin/env python3
"""Evaluate a working exercise source with a configured command."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class RequestError(ValueError):
    """Raised when a script request is invalid."""


def read_request() -> dict[str, Any]:
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise RequestError(f"invalid JSON request: {error.msg}") from error
    if not isinstance(request, dict):
        raise RequestError("request must be a JSON object")
    return request


def required_string(request: dict[str, Any], name: str) -> str:
    value = request.get(name)
    if not isinstance(value, str) or not value:
        raise RequestError(f"{name} must be a non-empty string")
    return value


def evaluation_command(request: dict[str, Any], source: Path) -> list[str]:
    value = request.get("command")
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(argument, str) or not argument for argument in value)
    ):
        raise RequestError("command must be a non-empty array of non-empty strings")
    if not any("{source}" in argument for argument in value):
        raise RequestError("command must contain a {source} placeholder")
    return [argument.replace("{source}", str(source)) for argument in value]


def diagnostics_for(result: subprocess.CompletedProcess[str]) -> str:
    streams = [stream.rstrip() for stream in (result.stdout, result.stderr) if stream]
    return "\n".join(stream for stream in streams if stream)


def evaluate_exercise(request: dict[str, Any]) -> dict[str, Any]:
    source = Path(required_string(request, "source_path")).expanduser()
    metadata = Path(required_string(request, "metadata_path")).expanduser()
    if not source.is_file():
        raise RequestError(f"working source does not exist: {source}")
    if not metadata.is_file():
        raise RequestError(f"metadata file does not exist: {metadata}")

    source = source.resolve()
    command = evaluation_command(request, source)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
    except FileNotFoundError as error:
        raise RequestError(f"evaluation command is not available: {command[0]}") from error
    except subprocess.TimeoutExpired:
        return {
            "compiled": False,
            "diagnostics": "Evaluation timed out after 30 seconds.",
            "metadata": metadata.read_text(encoding="utf-8"),
            "proposed_rating": "fail",
        }

    compiled = result.returncode == 0
    return {
        "compiled": compiled,
        "diagnostics": diagnostics_for(result),
        "metadata": metadata.read_text(encoding="utf-8"),
        "proposed_rating": "good" if compiled else "fail",
    }


def main() -> int:
    try:
        response = evaluate_exercise(read_request())
    except (OSError, RequestError, UnicodeError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1

    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
