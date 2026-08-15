#!/usr/bin/env python3
"""Codex CLI reviewer implementing the generic reviewer executable contract."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path
from reviewer_assets import (
    FOLLOW_UP_PROMPT_PATH,
    FOLLOW_UP_SCHEMA,
    PROMPT_PATH,
    SCHEMA,
    build_prompt as build_reviewer_prompt,
)

def build_prompt(request: dict, follow_up: bool = False) -> str:
    return build_reviewer_prompt(
        request,
        follow_up=follow_up,
        prompt_path=FOLLOW_UP_PROMPT_PATH if follow_up else PROMPT_PATH,
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--follow-up", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=("minimal", "low", "medium", "high", "xhigh"))
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    executable=os.environ.get("PRACTICE_CODEX","codex")
    if args.check:
        return subprocess.run([executable,"--version"],check=False).returncode
    request=json.load(sys.stdin)
    prompt=build_prompt(request, follow_up=args.follow_up)
    with tempfile.TemporaryDirectory(prefix="practice-review-") as directory:
        schema_path = Path(directory) / "review-schema.json"
        schema_path.write_text(json.dumps(FOLLOW_UP_SCHEMA if args.follow_up else SCHEMA), encoding="utf-8")
        command=[executable,"exec","--ephemeral","--sandbox","read-only","--skip-git-repo-check","--output-schema",str(schema_path),"--output-last-message",str(Path(directory)/"review.json")]
        model_environment = "PRACTICE_FOLLOW_UP_MODEL" if args.follow_up else "PRACTICE_REVIEW_MODEL"
        effort_environment = "PRACTICE_FOLLOW_UP_EFFORT" if args.follow_up else "PRACTICE_REVIEW_EFFORT"
        model=os.environ.get(model_environment) or args.model
        if model: command += ["--model",model]
        effort=os.environ.get(effort_environment) or args.effort
        if effort: command += ["--config",f'model_reasoning_effort="{effort}"']
        result=subprocess.run(command,input=prompt,text=True,capture_output=True,check=False,cwd=directory)
        output=Path(directory)/"review.json"
        if result.returncode or not output.is_file():
            sys.stderr.write(result.stderr or result.stdout); return result.returncode or 1
        sys.stdout.write(output.read_text()); sys.stdout.write("\n"); return 0
if __name__=="__main__": raise SystemExit(main())
