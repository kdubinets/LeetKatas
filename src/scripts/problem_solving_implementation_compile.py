#!/usr/bin/env python3
"""Syntax-check a saved implementation draft; compiler errors are normal results."""
from __future__ import annotations
import json, os, sqlite3, subprocess, sys, tempfile
from practice_scheduler import SchedulerError
from problem_solving_store import ProblemSolvingStore, problem_solving_database_path

def compile_draft(request: dict) -> dict:
    draft_id = request.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id: raise ValueError("draft_id is required")
    store = ProblemSolvingStore(problem_solving_database_path(request)); draft = store.draft(draft_id)
    if not draft: raise ValueError("draft not found")
    compiler = request.get("compiler") or os.environ.get("CXX") or "c++"
    if not isinstance(compiler, str) or not compiler: raise ValueError("compiler must be a non-empty string")
    with tempfile.TemporaryDirectory(prefix="level-c-implementation-") as directory:
        source = os.path.join(directory, "draft.cpp")
        with open(source, "w", encoding="utf-8") as output: output.write(draft["source"])
        try:
            result = subprocess.run([compiler, "-std=c++20", "-fsyntax-only", source], text=True, capture_output=True, timeout=30, check=False)
            diagnostics = "\n".join(x.strip() for x in (result.stderr, result.stdout) if x.strip())[:12000]
            status = "success" if result.returncode == 0 else "error"
            store.record_implementation_compile(draft_id, status, result.returncode, diagnostics)
            return {"draft_id": draft_id, "compiled": status == "success", "status": status, "exit_code": result.returncode, "diagnostics": diagnostics}
        except FileNotFoundError:
            store.record_implementation_compile(draft_id, "unavailable", None, "Compiler unavailable")
            return {"draft_id": draft_id, "compiled": False, "status": "unavailable", "exit_code": None, "diagnostics": "Compiler unavailable"}
        except subprocess.TimeoutExpired:
            store.record_implementation_compile(draft_id, "error", None, "Compilation timed out after 30 seconds")
            return {"draft_id": draft_id, "compiled": False, "status": "error", "exit_code": None, "diagnostics": "Compilation timed out after 30 seconds"}

def main() -> int:
    try: response = compile_draft(json.load(sys.stdin))
    except (ValueError, SchedulerError, sqlite3.Error, json.JSONDecodeError) as error:
        json.dump({"error":str(error)},sys.stdout);sys.stdout.write("\n");return 1
    json.dump(response,sys.stdout);sys.stdout.write("\n");return 0
if __name__ == "__main__": raise SystemExit(main())
