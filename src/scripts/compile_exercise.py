#!/usr/bin/env python3
"""Compile a practice working copy without submitting it for review."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


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


def compile_exercise(request: dict[str, Any]) -> dict[str, Any]:
    source_path = request.get("source_path")
    if not isinstance(source_path, str) or not source_path:
        raise RequestError("source_path must be a non-empty string")
    source = Path(source_path).expanduser()
    if not source.is_file():
        raise RequestError("source_path must exist")
    command = request.get("command")
    if (not isinstance(command, list) or not command
            or any(not isinstance(item, str) or not item for item in command)
            or not any("{source}" in item for item in command)):
        raise RequestError("command must contain a {source} placeholder")
    command = [item.replace("{source}", str(source.resolve())) for item in command]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=30)
        diagnostics = "\n".join(
            item.rstrip() for item in (result.stdout, result.stderr) if item and item.strip()
        )
        compiled = result.returncode == 0
    except FileNotFoundError as error:
        raise RequestError(f"evaluation command is not available: {command[0]}") from error
    except subprocess.TimeoutExpired:
        compiled, diagnostics = False, "Compilation timed out after 30 seconds."
    return {"compiled": compiled, "diagnostics": diagnostics, "command": command,
            "submitted_source": source.read_text(encoding="utf-8")}


def main() -> int:
    try:
        response = compile_exercise(read_request())
    except (OSError, UnicodeError, RequestError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
