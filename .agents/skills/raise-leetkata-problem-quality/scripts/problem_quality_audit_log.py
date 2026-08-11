#!/usr/bin/env python3
"""Maintain local, append-only audit records for LeetKatas problem-quality work."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def parse_artifacts(values: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    hashes: dict[str, str] = {}
    paths: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"artifact must be NAME=PATH: {value}")
        name, raw_path = value.split("=", 1)
        if not name or name in hashes:
            raise ValueError(f"artifact name must be unique and non-empty: {value}")
        path = Path(raw_path)
        if not path.is_file():
            raise ValueError(f"artifact does not exist or is not a file: {path}")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        paths[name] = str(path)
    return hashes, paths


def load_records(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSONL at {log_path}:{line_number}: {error.msg}") from error
        if not isinstance(record, dict):
            raise ValueError(f"record at {log_path}:{line_number} is not an object")
        records.append(record)
    return records


def latest_for(records: list[dict[str, Any]], difficulty: str, problem_id: int) -> dict[str, Any] | None:
    for record in reversed(records):
        if record.get("difficulty") == difficulty and record.get("problem_id") == problem_id:
            return record
    return None


def status(args: argparse.Namespace) -> None:
    hashes, _ = parse_artifacts(args.artifact)
    latest = latest_for(load_records(args.log), args.difficulty, args.problem_id)
    state = "missing" if latest is None else "current" if latest.get("artifact_hashes") == hashes else "stale"
    print(json.dumps({"state": state, "latest": latest, "artifact_hashes": hashes}, sort_keys=True))


def record(args: argparse.Namespace) -> None:
    hashes, paths = parse_artifacts(args.artifact)
    findings = dict(item.split("=", 1) for item in args.finding)
    expected = {"must_fix", "should_improve", "optional"}
    if set(findings) != expected or any(not value.isdigit() for value in findings.values()):
        raise ValueError("provide exactly must_fix=N, should_improve=N, and optional=N")
    entry = {
        "schema_version": 1,
        "audited_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "difficulty": args.difficulty,
        "problem_id": args.problem_id,
        "mode": args.mode,
        "scope": args.scope,
        "outcome": args.outcome,
        "findings": {key: int(value) for key, value in findings.items()},
        "artifact_paths": paths,
        "artifact_hashes": hashes,
        "changed_paths": args.changed,
        "validation": args.validation,
        "notes": args.note,
    }
    args.log.parent.mkdir(parents=True, exist_ok=True)
    with args.log.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, sort_keys=True) + "\n")
    print(json.dumps(entry, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--log", type=Path, default=Path("logs/problem-quality-audit.jsonl"))
    common.add_argument("--difficulty", required=True)
    common.add_argument("--problem-id", required=True, type=int)
    common.add_argument("--artifact", action="append", required=True, metavar="NAME=PATH")

    status_parser = subparsers.add_parser("status", parents=[common])
    status_parser.set_defaults(handler=status)

    record_parser = subparsers.add_parser("record", parents=[common])
    record_parser.add_argument("--mode", choices=("audit", "raise"), required=True)
    record_parser.add_argument("--scope", action="append", required=True)
    record_parser.add_argument("--outcome", required=True)
    record_parser.add_argument("--finding", action="append", required=True, metavar="LEVEL=N")
    record_parser.add_argument("--changed", action="append", default=[])
    record_parser.add_argument("--validation", action="append", default=[])
    record_parser.add_argument("--note", action="append", default=[])
    record_parser.set_defaults(handler=record)

    args = parser.parse_args()
    try:
        args.handler(args)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
