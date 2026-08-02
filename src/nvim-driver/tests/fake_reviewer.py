#!/usr/bin/env python3
"""Deterministic generic reviewer used by the headless Neovim workflow."""
import json
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--check":
    raise SystemExit(0)

request = json.load(sys.stdin)
compiled = request["validation"]["succeeded"]
submitted = request["submitted_source"]
target_language = request["target_environment"]["language"]
if target_language != {"name": "C++", "version": "C++20"}:
    raise ValueError("expected the collection target environment")
if not compiled:
    verdict = "minor_defect"
    summary = "The approach is sound, but a local syntax error prevents compilation."
    rating = "acceptable"
elif "return 0;" in submitted:
    verdict = "incorrect"
    summary = "The implementation compiles, but it returns the wrong answer."
    rating = "fail"
else:
    verdict = "correct"
    summary = "The submitted implementation is correct."
    rating = "good"

json.dump(
    {
        "verdict": verdict,
        "summary": summary,
        "correctness_analysis": "The validation evidence and implementation support the verdict.",
        "major_issues": ["The returned value does not satisfy the exercise."] if verdict == "incorrect" else [],
        "minor_issues": ["Compilation failed because of a local syntax error."] if not compiled else [],
        "code_quality_analysis": "The implementation is concise and idiomatic.",
        "proposed_rating": rating,
        "rating_explanation": "The rating follows the practice rubric.",
        "improved_implementation": "return 42;" if verdict != "correct" else None,
        "improvement_explanation": "This replacement compiles and returns the requested answer." if verdict != "correct" else None,
        "alternative_implementation": None,
        "alternative_explanation": None,
    },
    sys.stdout,
)
sys.stdout.write("\n")
