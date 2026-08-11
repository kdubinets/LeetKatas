#!/usr/bin/env python3
"""Codex CLI adapter for the dedicated Level C conversation contracts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PROMPTS = {
    "clarification": Path(__file__).with_name("prompts") / "level_c_clarification.txt",
    "discussion": Path(__file__).with_name("prompts") / "level_c_discussion.txt",
}
SCHEMAS = {
    "clarification": {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "answer", "disclosure"],
        "properties": {
            "status": {"type": "string", "enum": ["answered", "redirected"]},
            "answer": {"type": "string"},
            "disclosure": {"type": "string", "enum": ["clarification", "none"]},
        },
    },
    "discussion": {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "answer", "references", "follow_up_suggestions"],
        "properties": {
            "status": {"type": "string", "enum": ["answered"]},
            "answer": {"type": "string"},
            "references": {"type": "array", "items": {"type": "string"}},
            "follow_up_suggestions": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    },
}


def build_prompt(mode: str, request: dict) -> str:
    instructions = PROMPTS[mode].read_text(encoding="utf-8").rstrip()
    return instructions + "\n\nConversation context:\n" + json.dumps(request)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mode", choices=tuple(PROMPTS), required=False)
    parser.add_argument("--model")
    parser.add_argument(
        "--effort", choices=("minimal", "low", "medium", "high", "xhigh")
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    executable = os.environ.get("PRACTICE_CODEX", "codex")
    if args.check:
        return subprocess.run([executable, "--version"], check=False).returncode
    if args.mode is None:
        raise SystemExit("--mode is required")
    request = json.load(sys.stdin)
    prompt = build_prompt(args.mode, request)
    with tempfile.TemporaryDirectory(prefix="level-c-conversation-") as directory:
        root = Path(directory)
        schema_path = root / "schema.json"
        output_path = root / "response.json"
        schema_path.write_text(json.dumps(SCHEMAS[args.mode]), encoding="utf-8")
        command = [
            executable,
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
        ]
        if args.model:
            command += ["--model", args.model]
        if args.effort:
            command += ["--config", f'model_reasoning_effort="{args.effort}"']
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
            cwd=directory,
        )
        if result.returncode or not output_path.is_file():
            sys.stderr.write(result.stderr or result.stdout)
            return result.returncode or 1
        sys.stdout.write(output_path.read_text(encoding="utf-8"))
        sys.stdout.write("\n")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
