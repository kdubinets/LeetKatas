#!/usr/bin/env python3
"""Select the dedicated Codex implementation-review schema from request stage."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--model"); parser.add_argument("--effort")
    args = parser.parse_args(); request = json.load(sys.stdin); stage = request.get("stage")
    if stage not in {"checkpoint", "final"}: raise SystemExit("invalid implementation stage")
    command = [sys.executable, str(Path(__file__).with_name("level_c_codex.py")), "--mode", "implementation_" + stage]
    if args.model: command += ["--model", args.model]
    if args.effort: command += ["--effort", args.effort]
    return subprocess.run(command, input=json.dumps(request), text=True, check=False).returncode
if __name__ == "__main__": raise SystemExit(main())
