#!/usr/bin/env python3
"""Select an unseen-first, reproducible, ID-stratified C++ solution sample."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any


DEFAULT_LEDGER = Path("practice/cpp/audits/reviewed_solutions.json")


def numeric_solutions(root: Path, difficulty: str) -> list[Path]:
    directory = root / "problems" / difficulty / "solutions" / "cpp"
    return sorted(
        (path.relative_to(root) for path in directory.glob("*.cpp") if path.stem.isdecimal()),
        key=lambda path: int(path.stem),
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "solutions": {}}
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid audit ledger {path}: {error.msg}") from error
    if (
        not isinstance(ledger, dict)
        or ledger.get("schema_version") != 1
        or not isinstance(ledger.get("solutions"), dict)
    ):
        raise ValueError(f"invalid audit ledger schema: {path}")
    return ledger


def display_path(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def reviewed_unchanged(path: Path, root: Path, ledger: dict[str, Any]) -> bool:
    record = ledger["solutions"].get(str(path))
    return isinstance(record, dict) and record.get("sha256") == digest(root / path)


def allocate(total: int, buckets: int) -> list[int]:
    return [total // buckets + (index < total % buckets) for index in range(buckets)]


def stratified_sample(paths: list[Path], count: int, seed: int, label: str) -> list[Path]:
    if count >= len(paths):
        return paths
    bucket_count = min(5, len(paths), count)
    quotas = allocate(count, bucket_count)
    selected: list[Path] = []
    for index, quota in enumerate(quotas):
        start = index * len(paths) // bucket_count
        end = (index + 1) * len(paths) // bucket_count
        bucket = paths[start:end]
        random.Random(f"{seed}:{label}:{index}").shuffle(bucket)
        selected.extend(bucket[:quota])
    return sorted(selected, key=lambda path: int(path.stem))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--medium-count", type=int, default=36)
    parser.add_argument("--hard-count", type=int, default=24)
    args = parser.parse_args()
    if args.medium_count < 0 or args.hard_count < 0:
        parser.error("sample counts must be non-negative")

    root = args.root.resolve()
    ledger_path = args.ledger if args.ledger.is_absolute() else root / args.ledger
    try:
        ledger = load_ledger(ledger_path)
    except ValueError as error:
        parser.error(str(error))

    output: dict[str, Any] = {
        "seed": args.seed,
        "ledger": display_path(root, ledger_path),
        "source_counts": {},
        "selected": {},
    }
    for difficulty, requested in (("medium", args.medium_count), ("hard", args.hard_count)):
        paths = numeric_solutions(root, difficulty)
        eligible = [path for path in paths if not reviewed_unchanged(path, root, ledger)]
        selected = stratified_sample(eligible, requested, args.seed, difficulty)
        output["source_counts"][difficulty] = {
            "total": len(paths),
            "eligible": len(eligible),
            "unchanged_reviewed": len(paths) - len(eligible),
            "requested": requested,
            "selected": len(selected),
            "shortfall": requested - len(selected),
        }
        output["selected"][difficulty] = [
            {"path": str(path), "sha256": digest(root / path)} for path in selected
        ]
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
