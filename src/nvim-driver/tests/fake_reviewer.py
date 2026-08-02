#!/usr/bin/env python3
"""Deterministic generic reviewer used by the headless Neovim workflow."""
import json
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--check":
    raise SystemExit(0)

request = json.load(sys.stdin)
compiled = request["compiler"]["compiled"]
json.dump(
    {
        "verdict": "correct" if compiled else "incorrect",
        "summary": "The submitted implementation is correct." if compiled else "The submission does not compile.",
        "correctness_analysis": "The compiler evidence and implementation support the verdict.",
        "major_issues": [] if compiled else ["Compilation failed."],
        "minor_issues": [],
        "code_quality_analysis": "The implementation is concise and idiomatic.",
        "proposed_rating": "good" if compiled else "fail",
        "rating_explanation": "The rating follows the practice rubric.",
        "improved_implementation": None,
        "improvement_explanation": None,
        "alternative_implementation": None,
        "alternative_explanation": None,
    },
    sys.stdout,
)
sys.stdout.write("\n")
