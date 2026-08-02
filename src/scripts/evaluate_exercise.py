#!/usr/bin/env python3
"""Compile a submission, then pass all evidence to a replaceable reviewer."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Any
from reviewer_protocol import ReviewerError, configured_reviewer, review_request

class RequestError(ValueError): pass
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
    reviewer_command,name=configured_reviewer(request)
    if reviewer_command:
        evidence={"starter_source":starter.read_text(encoding="utf-8"),"submitted_source":source.read_text(encoding="utf-8"),"metadata":metadata_text,"compiler":{"command":command,"compiled":compiled,"diagnostics":diagnostics}}
        review=review_request(evidence,reviewer_command,progress=progress)
    else:
        progress("review_finished", status="unavailable", attempts=0)
        review={"status":"unavailable","attempts":0,"feedback":None,"failure":"no reviewer configured"}
    feedback=review["feedback"]
    progress("evaluation_finished")
    return {"compiled":compiled,"diagnostics":diagnostics,"metadata":metadata_text,"review":{**review,"reviewer":name},"proposed_rating":feedback.get("proposed_rating") if feedback else None}
def main():
    try: response=evaluate(read_request())
    except (OSError,UnicodeError,RequestError,ReviewerError) as e: json.dump({"error":str(e)},sys.stdout); sys.stdout.write("\n"); return 1
    json.dump(response,sys.stdout); sys.stdout.write("\n"); return 0
if __name__=="__main__": raise SystemExit(main())
