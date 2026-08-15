#!/usr/bin/env python3
"""Compile a submission, then pass all evidence to a replaceable reviewer."""
from __future__ import annotations
import json, subprocess, sys
import re
from pathlib import Path
from typing import Any
from practice_environment import TargetEnvironmentError, validate_target_environment
from reviewer_protocol import ReviewerError, configured_reviewer, review_request
from openai_pricing import priced_usage

class RequestError(ValueError): pass

HEADING = re.compile(r"^#\s+(.+?)\s*$")
FENCE = re.compile(r"^```([^`]*)$")

def parse_metadata_sections(metadata: str) -> list[dict[str, Any]]:
    """Best-effort extraction of level-one sections and fenced code."""
    source_lines = metadata.splitlines()
    sections: list[dict[str, Any]] = []
    section: dict[str, Any] | None = None
    text_lines: list[str] = []
    text_start = 0
    code_lines: list[str] | None = None
    code_start = 0
    code_language = ""

    def flush_text() -> None:
        nonlocal text_lines
        if section is not None and text_lines:
            section["blocks"].append({
                "type": "text", "start_line": text_start, "lines": text_lines,
            })
        text_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        if section is not None and code_lines is not None:
            section["blocks"].append({
                "type": "code", "language": code_language,
                "start_line": code_start, "lines": code_lines,
            })
        code_lines = None

    for line_number, line in enumerate(source_lines, 1):
        if code_lines is not None:
            if line.strip() == "```":
                flush_code()
            else:
                code_lines.append(line)
            continue

        heading = HEADING.match(line)
        if heading:
            flush_text()
            section = {
                "title": heading.group(1), "heading_line": line_number, "blocks": [],
            }
            sections.append(section)
            continue

        fence = FENCE.match(line)
        if section is not None and fence:
            flush_text()
            code_language = fence.group(1).strip()
            code_start = line_number + 1
            code_lines = []
            continue

        if section is not None:
            if not text_lines:
                text_start = line_number
            text_lines.append(line)

    if code_lines is not None:
        flush_code()
    else:
        flush_text()
    return sections

def read_request():
    try: value=json.load(sys.stdin)
    except json.JSONDecodeError as e: raise RequestError(f"invalid JSON request: {e.msg}") from e
    if not isinstance(value,dict): raise RequestError("request must be a JSON object")
    return value
def required(request,name):
    value=request.get(name)
    if not isinstance(value,str) or not value: raise RequestError(f"{name} must be a non-empty string")
    return value
def progress_reporter(request: dict[str, Any]):
    value = request.get("progress_path")
    if value is None:
        return lambda event, **fields: None
    if not isinstance(value, str) or not value:
        raise RequestError("progress_path must be a non-empty string when provided")
    path = Path(value).expanduser()
    sequence = 0
    def report(event: str, **fields: Any) -> None:
        nonlocal sequence
        sequence += 1
        record = {"sequence": sequence, "event": event, **fields}
        try:
            with path.open("a", encoding="utf-8") as output:
                output.write(json.dumps(record) + "\n")
        except OSError:
            pass
    return report
def evaluate(request: dict[str,Any]):
    progress = progress_reporter(request)
    source=Path(required(request,"source_path")).expanduser(); starter=Path(request.get("starter_source_path",source)).expanduser(); metadata=Path(required(request,"metadata_path")).expanduser()
    if not source.is_file() or not starter.is_file() or not metadata.is_file(): raise RequestError("source, starter source, and metadata files must exist")
    command=request.get("command")
    if not isinstance(command,list) or not command or any(not isinstance(x,str) or not x for x in command) or not any("{source}" in x for x in command): raise RequestError("command must contain a {source} placeholder")
    command=[x.replace("{source}",str(source.resolve())) for x in command]
    progress("compilation_started")
    try:
        result=subprocess.run(command,capture_output=True,text=True,check=False,timeout=30)
        compiled=result.returncode==0; diagnostics="\n".join(x.rstrip() for x in (result.stdout,result.stderr) if x and x.strip())
    except FileNotFoundError as e: raise RequestError(f"evaluation command is not available: {command[0]}") from e
    except subprocess.TimeoutExpired: compiled=False; diagnostics="Evaluation timed out after 30 seconds."
    progress("compilation_finished", compiled=compiled)
    metadata_text=metadata.read_text(encoding="utf-8")
    target_environment = request.get("target_environment")
    if target_environment is not None:
        target_environment = validate_target_environment(target_environment)
    submitted_source=source.read_text(encoding="utf-8")
    reviewer_command,name=configured_reviewer(request)
    reviewer_config = request.get("reviewer")
    reviewer_model = reviewer_config.get("model") if isinstance(reviewer_config, dict) and isinstance(reviewer_config.get("model"), str) else None
    reviewer_reasoning_effort = reviewer_config.get("reasoning_effort") if isinstance(reviewer_config, dict) and isinstance(reviewer_config.get("reasoning_effort"), str) else None
    reviewer_service_tier = reviewer_config.get("service_tier") if isinstance(reviewer_config, dict) and isinstance(reviewer_config.get("service_tier"), str) else None
    if reviewer_command:
        evidence={"starter_source":starter.read_text(encoding="utf-8"),"submitted_source":submitted_source,"exercise_metadata":metadata_text,"target_environment":target_environment,"validation":{"command":command,"succeeded":compiled,"diagnostics":diagnostics}}
        review=review_request(evidence,reviewer_command,progress=progress)
    else:
        progress("review_finished", status="unavailable", attempts=0)
        review={"status":"unavailable","attempts":0,"feedback":None,"failure":"no reviewer configured"}
    feedback=review["feedback"]
    progress("evaluation_finished")
    actual_tier = review.get("telemetry", {}).get("actual_service_tier") if isinstance(review.get("telemetry"), dict) else None
    service_tier = actual_tier or reviewer_service_tier
    usage = priced_usage(reviewer_model, service_tier, review.get("telemetry"))
    return {"compiled":compiled,"diagnostics":diagnostics,"metadata":metadata_text,"metadata_sections":parse_metadata_sections(metadata_text),"submitted_source":submitted_source,"review":{**review,"reviewer":name,"model":reviewer_model,"reasoning_effort":reviewer_reasoning_effort,"service_tier":service_tier,"usage":usage},"proposed_rating":feedback.get("proposed_rating") if feedback else None}
def main():
    try: response=evaluate(read_request())
    except (OSError,UnicodeError,RequestError,ReviewerError,TargetEnvironmentError) as e: json.dump({"error":str(e)},sys.stdout); sys.stdout.write("\n"); return 1
    json.dump(response,sys.stdout); sys.stdout.write("\n"); return 0
if __name__=="__main__": raise SystemExit(main())
