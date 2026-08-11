#!/usr/bin/env python3
"""Deterministic Level C conversation adapter for protocol and headless tests."""

from __future__ import annotations

import json
import sys


if len(sys.argv) > 1 and sys.argv[1] == "--check":
    raise SystemExit(0)

request = json.load(sys.stdin)
question = request["question"]
if question == "UNAVAILABLE":
    sys.stderr.write("private adapter failure body that must not be logged")
    raise SystemExit(1)

problem = request["problem"]
if "solution_outline" in problem:
    json.dump(
        {
            "status": "answered",
            "answer": "The invariant holds because each processed position preserves the stated boundary.",
            "references": ["outline:state_and_invariant", "outline:correctness"],
            "follow_up_suggestions": ["Which edge case exercises that boundary?"],
        },
        sys.stdout,
    )
elif "algorithm" in question.lower() or "approach" in question.lower():
    json.dump(
        {
            "status": "redirected",
            "answer": "That would reveal solving guidance. Request the optional hint or reveal the outline.",
            "disclosure": "none",
        },
        sys.stdout,
    )
else:
    json.dump(
        {
            "status": "answered",
            "answer": "The digits are stored least-significant first, beginning at the head.",
            "disclosure": "clarification",
        },
        sys.stdout,
    )
sys.stdout.write("\n")
