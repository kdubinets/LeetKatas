#!/usr/bin/env python3
"""Validate a language-neutral Level C problem-solving collection."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COLLECTION_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)+$")
PROBLEM_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)

CARD_KEYS = {"schema_version", "id", "source", "teaching"}
SOURCE_KEYS = {
    "provider",
    "problem_id",
    "title",
    "difficulty",
    "url",
    "local_path",
    "content_sha256",
}
TEACHING_KEYS = {
    "hint",
    "solution_outline",
    "accepted_alternatives",
    "tags",
    "prerequisites",
    "common_wrong_turns",
    "source_fidelity_notes",
}
OUTLINE_KEYS = {
    "decisive_insight",
    "approach",
    "state_and_invariant",
    "correctness",
    "complexity",
    "pitfall",
}
ARRAY_FIELDS = {
    "accepted_alternatives",
    "tags",
    "prerequisites",
    "common_wrong_turns",
    "source_fidelity_notes",
}
BRIEF_PRIVATE_MARKERS = {
    "accepted_alternatives",
    "common_wrong_turns",
    "content_sha256",
    "decisive_insight",
    "solution_outline",
    "source_fidelity_notes",
    "state_and_invariant",
}


class CollectionValidationError(ValueError):
    """Raised when a Level C collection violates its versioned contract."""


def require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CollectionValidationError(f"{context} must be a JSON object")
    return value


def require_exact_keys(
    value: dict[str, Any], required: set[str], context: str
) -> None:
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required)
    if missing:
        raise CollectionValidationError(
            f"{context} is missing required field: {missing[0]}"
        )
    if unknown:
        raise CollectionValidationError(
            f"{context} contains unknown field: {unknown[0]}"
        )


def require_nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CollectionValidationError(f"{context} must be a nonempty string")
    return value


def read_json(path: Path, context: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise CollectionValidationError(f"missing {context}: {path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CollectionValidationError(f"could not read {context} {path}: {error}") from error
    return require_object(value, context)


def validate_collection_metadata(collection: Path) -> str:
    document = read_json(collection / "collection.json", "collection metadata")
    require_exact_keys(document, {"schema_version", "id"}, "collection metadata")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise CollectionValidationError("unsupported collection schema_version")
    identity = require_nonempty_string(document["id"], "collection id")
    if not COLLECTION_ID_PATTERN.fullmatch(identity):
        raise CollectionValidationError("collection id is not a stable global identifier")
    return identity


def validate_order(collection: Path) -> list[str]:
    path = collection / "problem_order.md"
    try:
        problem_ids = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise CollectionValidationError(f"could not read problem order {path}: {error}") from error
    if not problem_ids:
        raise CollectionValidationError("problem order contains no problem IDs")
    for line_number, problem_id in enumerate(problem_ids, start=1):
        if not PROBLEM_ID_PATTERN.fullmatch(problem_id):
            raise CollectionValidationError(
                f"invalid problem ID in {path} at line {line_number}"
            )
    duplicates = sorted(
        problem_id
        for problem_id in set(problem_ids)
        if problem_ids.count(problem_id) > 1
    )
    if duplicates:
        raise CollectionValidationError(
            "problem order contains duplicate problem IDs: " + ", ".join(duplicates)
        )
    return problem_ids


def validate_card_files(collection: Path, problem_ids: list[str]) -> Path:
    cards = collection / "cards"
    if not cards.is_dir():
        raise CollectionValidationError(f"missing cards directory: {cards}")

    brief_ids = {path.name.removesuffix(".brief.md") for path in cards.glob("*.brief.md")}
    record_ids = {path.name.removesuffix(".card.json") for path in cards.glob("*.card.json")}
    ordered_ids = set(problem_ids)
    for label, discovered in (("brief", brief_ids), ("card", record_ids)):
        missing = sorted(ordered_ids - discovered)
        unknown = sorted(discovered - ordered_ids)
        if missing:
            raise CollectionValidationError(
                f"problem order is missing a matching {label} file for: " + ", ".join(missing)
            )
        if unknown:
            raise CollectionValidationError(
                f"cards directory contains unordered {label} files for: " + ", ".join(unknown)
            )

    recognized = {
        f"{problem_id}.brief.md" for problem_id in problem_ids
    } | {f"{problem_id}.card.json" for problem_id in problem_ids}
    unexpected = sorted(path.name for path in cards.iterdir() if path.name not in recognized)
    if unexpected:
        raise CollectionValidationError(
            f"cards directory contains unexpected entry: {unexpected[0]}"
        )
    return cards


def validate_brief(path: Path, expected_title: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise CollectionValidationError(f"could not read problem brief {path}: {error}") from error
    lines = text.splitlines()
    if not lines or lines[0] != f"# {expected_title}":
        raise CollectionValidationError(
            f"problem brief title does not match source title: {path}"
        )
    if not any(line.strip() for line in lines[1:]):
        raise CollectionValidationError(f"problem brief has no focused content: {path}")
    if URL_PATTERN.search(text) or re.search(r"(?im)^\s*source\s*:", text):
        raise CollectionValidationError(f"problem brief exposes source attribution: {path}")
    normalized = text.casefold().replace(" ", "_").replace("-", "_")
    leaked = sorted(marker for marker in BRIEF_PRIVATE_MARKERS if marker in normalized)
    if leaked:
        raise CollectionValidationError(
            f"problem brief exposes private teaching field {leaked[0]}: {path}"
        )


def resolve_source(source_root: Path, local_path: str) -> Path:
    relative = Path(local_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise CollectionValidationError("source.local_path must stay within source_root")
    root = source_root.resolve()
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        raise CollectionValidationError("source.local_path must stay within source_root")
    if not resolved.is_file():
        raise CollectionValidationError(f"source.local_path does not exist: {local_path}")
    return resolved


def validate_card(path: Path, expected_id: str, source_root: Path) -> str:
    document = read_json(path, "card record")
    require_exact_keys(document, CARD_KEYS, f"card {expected_id}")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise CollectionValidationError(f"unsupported schema_version in card {expected_id}")
    card_id = require_nonempty_string(document["id"], f"card {expected_id} id")
    if card_id != expected_id:
        raise CollectionValidationError(
            f"card ID {card_id} does not match filename ID {expected_id}"
        )

    source = require_object(document["source"], f"card {expected_id} source")
    require_exact_keys(source, SOURCE_KEYS, f"card {expected_id} source")
    for name in SOURCE_KEYS - {"content_sha256"}:
        require_nonempty_string(source[name], f"card {expected_id} source.{name}")
    if source["difficulty"] not in {"easy", "medium", "hard"}:
        raise CollectionValidationError(
            f"card {expected_id} source.difficulty must be easy, medium, or hard"
        )
    if not URL_PATTERN.match(source["url"]):
        raise CollectionValidationError(f"card {expected_id} source.url must be an HTTP URL")
    expected_hash = require_nonempty_string(
        source["content_sha256"], f"card {expected_id} source.content_sha256"
    )
    if not SHA256_PATTERN.fullmatch(expected_hash):
        raise CollectionValidationError(
            f"card {expected_id} source.content_sha256 must be lowercase SHA-256"
        )
    source_path = resolve_source(source_root, source["local_path"])
    try:
        source_bytes = source_path.read_bytes()
    except OSError as error:
        raise CollectionValidationError(
            f"could not read source.local_path {source['local_path']}: {error}"
        ) from error
    actual_hash = hashlib.sha256(source_bytes).hexdigest()
    if actual_hash != expected_hash:
        raise CollectionValidationError(
            f"card {expected_id} source hash is stale for {source['local_path']}"
        )

    teaching = require_object(document["teaching"], f"card {expected_id} teaching")
    require_exact_keys(teaching, TEACHING_KEYS, f"card {expected_id} teaching")
    require_nonempty_string(teaching["hint"], f"card {expected_id} teaching.hint")
    outline = require_object(
        teaching["solution_outline"], f"card {expected_id} solution_outline"
    )
    require_exact_keys(outline, OUTLINE_KEYS, f"card {expected_id} solution_outline")
    for name in OUTLINE_KEYS:
        require_nonempty_string(outline[name], f"card {expected_id} solution_outline.{name}")
    for name in ARRAY_FIELDS:
        values = teaching[name]
        if not isinstance(values, list) or any(
            not isinstance(value, str) or not value.strip() for value in values
        ):
            raise CollectionValidationError(
                f"card {expected_id} teaching.{name} must be an array of nonempty strings"
            )
    return source["title"]


def validate_collection(
    collection_directory: str | Path, source_root: str | Path = REPOSITORY_ROOT
) -> dict[str, Any]:
    collection = Path(collection_directory).expanduser()
    if not collection.is_dir():
        raise CollectionValidationError(
            f"collection_directory does not exist: {collection}"
        )
    if not (collection / "collection_spec.md").is_file():
        raise CollectionValidationError(
            f"missing collection specification: {collection / 'collection_spec.md'}"
        )
    collection_id = validate_collection_metadata(collection)
    problem_ids = validate_order(collection)
    cards = validate_card_files(collection, problem_ids)
    root = Path(source_root).expanduser()
    if not root.is_dir():
        raise CollectionValidationError(f"source_root does not exist: {root}")
    for problem_id in problem_ids:
        title = validate_card(cards / f"{problem_id}.card.json", problem_id, root)
        validate_brief(cards / f"{problem_id}.brief.md", title)
    return {
        "status": "ok",
        "collection_id": collection_id,
        "card_count": len(problem_ids),
        "problem_ids": problem_ids,
    }


def required_string(request: dict[str, Any], name: str) -> str:
    value = request.get(name)
    if not isinstance(value, str) or not value:
        raise CollectionValidationError(f"{name} must be a nonempty string")
    return value


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise CollectionValidationError("request must be a JSON object")
        unknown = sorted(set(request) - {"collection_directory", "source_root"})
        if unknown:
            raise CollectionValidationError(
                f"request contains unknown field: {unknown[0]}"
            )
        source_root = request.get("source_root", str(REPOSITORY_ROOT))
        if not isinstance(source_root, str) or not source_root:
            raise CollectionValidationError("source_root must be a nonempty string")
        response = validate_collection(
            required_string(request, "collection_directory"), source_root
        )
        json.dump(response, sys.stdout)
        sys.stdout.write("\n")
        return 0
    except (CollectionValidationError, json.JSONDecodeError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
