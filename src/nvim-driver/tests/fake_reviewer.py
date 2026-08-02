#!/usr/bin/env python3
"""Deterministic generic reviewer used by the headless Neovim workflow."""
import json
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--check":
    raise SystemExit(0)

request = json.load(sys.stdin)
if "question" in request:
    if not isinstance(request.get("initial_review"), dict):
        raise ValueError("expected the initial review")
    if not isinstance(request.get("messages"), list):
        raise ValueError("expected bounded conversation history")
    json.dump(
        {"answer": "The answer follows from the exercise requirement and your return statement."},
        sys.stdout,
    )
    sys.stdout.write("\n")
    raise SystemExit(0)

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
        "minor_issues": [
            "Compilation failed because of a local syntax error.\n"
            "Fix the missing returned expression and resubmit."
        ] if not compiled else [],
        "code_quality_analysis": "The implementation is concise and idiomatic.",
        "proposed_rating": rating,
        "rating_explanation": "The rating follows the practice rubric.",
        "improved_implementation": (
            "return 40 + 2;" if verdict == "correct" else "return 42;"
        ),
        "improvement_explanation": (
            "This equivalent form demonstrates that correct reviews may include an improvement."
            if verdict == "correct"
            else "This replacement compiles and returns the requested answer."
        ),
        "alternative_implementation": None,
        "alternative_explanation": None,
        "version_notes": (
            "Later versions: prefer the newer direct standard facility when it is available.\n"
            "Earlier versions: use the established C++17-compatible idiom."
            if verdict == "correct" else None
        ),
    },
    sys.stdout,
)
sys.stdout.write("\n")
