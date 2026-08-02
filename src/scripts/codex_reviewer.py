#!/usr/bin/env python3
"""Codex CLI reviewer implementing the generic reviewer executable contract."""
from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

PROMPT_PATH = Path(__file__).with_name("prompts") / "codex_reviewer.txt"

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["verdict", "summary", "correctness_analysis", "major_issues", "minor_issues", "code_quality_analysis", "proposed_rating", "rating_explanation", "improved_implementation", "improvement_explanation", "alternative_implementation", "alternative_explanation"],
    "properties": {
        "verdict": {"type": "string", "enum": ["correct", "minor_defect", "incorrect", "cannot_assess"]},
        "summary": {"type": "string"},
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
    },
}
def build_prompt(request: dict) -> str:
    instructions = PROMPT_PATH.read_text(encoding="utf-8").rstrip()
    return instructions + "\n\nReview evidence:\n" + json.dumps(request)

def main() -> int:
    executable=os.environ.get("PRACTICE_CODEX","codex")
    if len(sys.argv)>1 and sys.argv[1]=="--check":
        return subprocess.run([executable,"--version"],check=False).returncode
    request=json.load(sys.stdin)
    prompt=build_prompt(request)
    with tempfile.TemporaryDirectory(prefix="practice-review-") as directory:
        schema_path = Path(directory) / "review-schema.json"
        schema_path.write_text(json.dumps(SCHEMA), encoding="utf-8")
        command=[executable,"exec","--ephemeral","--sandbox","read-only","--skip-git-repo-check","--output-schema",str(schema_path),"--output-last-message",str(Path(directory)/"review.json")]
        model=os.environ.get("PRACTICE_REVIEW_MODEL")
        if model: command += ["--model",model]
        result=subprocess.run(command,input=prompt,text=True,capture_output=True,check=False,cwd=directory)
        output=Path(directory)/"review.json"
        if result.returncode or not output.is_file():
            sys.stderr.write(result.stderr or result.stdout); return result.returncode or 1
        sys.stdout.write(output.read_text()); sys.stdout.write("\n"); return 0
if __name__=="__main__": raise SystemExit(main())
