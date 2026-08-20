"""Shared prompts and output schemas for practice reviewer adapters."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_reviewer.txt"
FOLLOW_UP_PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_review_follow_up.txt"
COMPILER_FOLLOW_UP_PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_compiler_follow_up.txt"

SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["correctness_analysis", "code_quality_analysis", "major_issues", "minor_issues", "verdict", "proposed_rating", "rating_explanation", "summary", "improved_implementation", "improvement_explanation", "alternative_implementation", "alternative_explanation", "version_notes"],
    "properties": {
        "correctness_analysis": {"type": "string"},
        "code_quality_analysis": {"type": "string"},
        "major_issues": {"type": "array", "items": {"type": "string"}},
        "minor_issues": {"type": "array", "items": {"type": "string"}},
        "verdict": {"type": "string", "enum": ["correct", "minor_defect", "incorrect", "cannot_assess"]},
        "proposed_rating": {"type": ["string", "null"], "enum": ["fail", "acceptable", "good", "excellent", None]},
        "rating_explanation": {"type": "string"},
        "summary": {"type": "string", "description": "One or two learner-facing plain-text sentences with no Markdown decoration, stating the most important correctness point."},
        "improved_implementation": {"type": ["string", "null"]},
        "improvement_explanation": {"type": ["string", "null"]},
        "alternative_implementation": {"type": ["string", "null"]},
        "alternative_explanation": {"type": ["string", "null"]},
        "version_notes": {"type": ["string", "null"]},
    },
}
FOLLOW_UP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer"],
    "properties": {"answer": {"type": "string"}},
}


def build_prompt(
    request: dict[str, Any], follow_up: bool = False, prompt_path: Path | None = None,
    compiler_follow_up: bool = False,
) -> str:
    instructions = load_instructions(follow_up=follow_up, prompt_path=prompt_path,
                                     compiler_follow_up=compiler_follow_up)
    label = "Compiler question context" if compiler_follow_up else (
        "Follow-up context" if follow_up else "Review evidence")
    return instructions + f"\n\n{label}:\n" + json.dumps(request)


def load_instructions(follow_up: bool = False, prompt_path: Path | None = None,
                      compiler_follow_up: bool = False) -> str:
    selected_path = prompt_path or (COMPILER_FOLLOW_UP_PROMPT_PATH if compiler_follow_up
                                    else FOLLOW_UP_PROMPT_PATH if follow_up else PROMPT_PATH)
    return selected_path.read_text(encoding="utf-8").rstrip()
