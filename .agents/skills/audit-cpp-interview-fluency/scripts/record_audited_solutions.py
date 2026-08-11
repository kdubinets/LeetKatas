#!/usr/bin/env python3
"""Record a completed audit sample in the hash-aware solution ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from select_solved_cpp_sample import DEFAULT_LEDGER, load_ledger


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(root: Path, value: Path, label: str) -> str:
    resolved = value.resolve()
    try:
        return str(resolved.relative_to(root))
    except ValueError as error:
        raise ValueError(f"{label} must be inside the repository: {value}") from error


def selected_entries(manifest: dict[str, Any]) -> list[dict[str, str]]:
    selected = manifest.get("selected")
    if not isinstance(selected, dict):
        raise ValueError("sample manifest has no selected solutions")
    entries: list[dict[str, str]] = []
    for difficulty in ("medium", "hard"):
        values = selected.get(difficulty)
        if not isinstance(values, list):
            raise ValueError(f"sample manifest has invalid {difficulty} selection")
        for value in values:
            if (
                not isinstance(value, dict)
                or not isinstance(value.get("path"), str)
                or not isinstance(value.get("sha256"), str)
            ):
                raise ValueError("sample manifest has an invalid selected solution")
            entries.append({"path": value["path"], "sha256": value["sha256"]})
    return entries


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        json.dump(value, temporary, indent=2, sort_keys=True)
        temporary.write("\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--recorded-at", required=True, help="ISO date, for example 2026-08-09")
    args = parser.parse_args()
    try:
        date.fromisoformat(args.recorded_at)
    except ValueError as error:
        parser.error(f"invalid --recorded-at date: {error}")

    root = args.root.resolve()
    ledger_path = args.ledger if args.ledger.is_absolute() else root / args.ledger
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    report_path = args.report if args.report.is_absolute() else root / args.report
    if not report_path.is_file():
        parser.error(f"report does not exist: {report_path}")
    report = relative_path(root, report_path, "report")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = selected_entries(manifest)
        ledger = load_ledger(ledger_path)
        for entry in entries:
            path = Path(entry["path"])
            if (
                path.is_absolute()
                or len(path.parts) != 5
                or path.parts[0] != "problems"
                or path.parts[1] not in {"medium", "hard"}
                or path.parts[2:4] != ("solutions", "cpp")
            ):
                raise ValueError(f"invalid solution path in sample manifest: {path}")
            source = root / path
            if not source.is_file() or source.suffix != ".cpp" or not source.stem.isdecimal():
                raise ValueError(f"solution no longer exists: {path}")
            if digest(source) != entry["sha256"]:
                raise ValueError(f"solution changed since sampling: {path}")
            record = ledger["solutions"].setdefault(str(path), {"sha256": entry["sha256"], "audits": []})
            record["sha256"] = entry["sha256"]
            audit = {"report": report, "recorded_at": args.recorded_at, "sha256": entry["sha256"]}
            if audit not in record["audits"]:
                record["audits"].append(audit)
        atomic_write(ledger_path, ledger)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
