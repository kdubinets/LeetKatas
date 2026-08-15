"""Shared prompts and output schemas for practice reviewer adapters."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_reviewer.txt"
FOLLOW_UP_PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_review_follow_up.txt"

SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["verdict", "summary", "correctness_analysis", "major_issues", "minor_issues", "code_quality_analysis", "proposed_rating", "rating_explanation", "improved_implementation", "improvement_explanation", "alternative_implementation", "alternative_explanation", "version_notes"],
    "properties": {
        "verdict": {"type": "string", "enum": ["correct", "minor_defect", "incorrect", "cannot_assess"]},
        "summary": {"type": "string", "description": "One or two learner-facing plain-text sentences with no Markdown decoration, stating the most important correctness point."},
        "correctness_analysis": {"type": "string"},
        "major_issues": {"type": "array", "items": {"type": "string"}},
        "minor_issues": {"type": "array", "items": {"type": "string"}},
        "code_quality_analysis": {"type": "string"},
        "proposed_rating": {"type": ["string", "null"], "enum": ["fail", "acceptable", "good", "excellent", None]},
        "rating_explanation": {"type": "string"},
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
    request: dict[str, Any], follow_up: bool = False, prompt_path: Path | None = None
) -> str:
    instructions = load_instructions(follow_up=follow_up, prompt_path=prompt_path)
    label = "Follow-up context" if follow_up else "Review evidence"
    return instructions + f"\n\n{label}:\n" + json.dumps(request)


def load_instructions(follow_up: bool = False, prompt_path: Path | None = None) -> str:
    selected_path = prompt_path or (FOLLOW_UP_PROMPT_PATH if follow_up else PROMPT_PATH)
    return selected_path.read_text(encoding="utf-8").rstrip()
