#!/usr/bin/env python3
"""Disable, re-enable, or permanently remove a practice exercise pair."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

from practice_scheduler import PracticeStore, SchedulerError, collection_keys, database_path


class RequestError(ValueError):
    """Raised when an exercise-management request is invalid."""


def read_request() -> dict[str, Any]:
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise RequestError(f"invalid JSON request: {error.msg}") from error
    if not isinstance(request, dict):
        raise RequestError("request must be a JSON object")
    return request


def required_string(request: dict[str, Any], name: str) -> str:
    value = request.get(name)
    if not isinstance(value, str) or not value:
        raise RequestError(f"{name} must be a non-empty string")
    return value


def exercise_paths(collection: Path, exercise_id: str, source_extension: str,
                   metadata_extension: str) -> tuple[Path, Path]:
    if not source_extension.startswith(".") or not metadata_extension.startswith("."):
        raise RequestError("source_extension and metadata_extension must start with a dot")
    if Path(exercise_id).name != exercise_id or exercise_id in {".", ".."}:
        raise RequestError("exercise_id must be a plain filename stem")
    source = collection / f"{exercise_id}{source_extension}"
    metadata = collection / f"{exercise_id}{metadata_extension}"
    if not source.is_file() or not metadata.is_file():
        raise RequestError(f"exercise pair does not exist: {exercise_id}")
    return source, metadata


def remove_manifest_row(manifest: Path, exercise_id: str) -> str:
    lines = manifest.read_text(encoding="utf-8").splitlines(keepends=True)
    marker = f"| `{exercise_id}` |"
    retained = [line for line in lines if marker not in line]
    if len(retained) != len(lines) - 1:
        raise RequestError(f"exercise manifest must contain exactly one row for {exercise_id}")
    return "".join(retained)


def remove_order_entry(order_file: Path, exercise_id: str) -> str | None:
    if not order_file.is_file():
        return None
    lines = order_file.read_text(encoding="utf-8").splitlines(keepends=True)
    retained = [line for line in lines if line.rstrip("\r\n") != exercise_id]
    if len(retained) != len(lines) - 1:
        raise RequestError(f"exercise order must contain exactly one entry for {exercise_id}")
    return "".join(retained)


def manage_exercise(request: dict[str, Any]) -> dict[str, str | bool]:
    action = required_string(request, "action")
    if action not in {"disable", "enable", "delete"}:
        raise RequestError("action must be disable, enable, or delete")
    exercise_id = required_string(request, "exercise_id")
    path_key, collection_key, _ = collection_keys(request.get("exercise_directory"))
    collection = Path(path_key)
    source, metadata = exercise_paths(
        collection, exercise_id, required_string(request, "source_extension"),
        required_string(request, "metadata_extension"),
    )
    store = PracticeStore(database_path(request))
    store.adopt_collection_key(path_key, collection_key)

    if action == "disable":
        store.disable_exercise(collection_key, exercise_id)
        return {"managed": True, "action": action, "exercise_id": exercise_id}
    if action == "enable":
        store.enable_exercise(collection_key, exercise_id)
        return {"managed": True, "action": action, "exercise_id": exercise_id}

    manifest = collection / "exercise_manifest.md"
    if not manifest.is_file():
        raise RequestError(f"exercise manifest does not exist: {manifest}")
    new_manifest = remove_manifest_row(manifest, exercise_id)
    order_file = collection / "exercise_order.md"
    new_order = remove_order_entry(order_file, exercise_id)

    # Exclude first: if a later filesystem operation fails, the bad exercise
    # cannot be selected while the collection is repaired.
    store.disable_exercise(collection_key, exercise_id)
    source.unlink()
    metadata.unlink()
    manifest.write_text(new_manifest, encoding="utf-8")
    if new_order is not None:
        order_file.write_text(new_order, encoding="utf-8")
    return {"managed": True, "action": action, "exercise_id": exercise_id}


def main() -> int:
    try:
        response = manage_exercise(read_request())
    except (OSError, RequestError, SchedulerError, sqlite3.Error, UnicodeError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
