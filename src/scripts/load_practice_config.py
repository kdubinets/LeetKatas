#!/usr/bin/env python3
"""Load and validate the user-facing practice TOML configuration."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib


class ConfigError(ValueError):
    pass


SCHEMA: dict[str, dict[str, type]] = {
    "practice": {
        "collection": str,
        "collections": list,
        "database_path": str,
        "log_path": str,
        "notes_directory": str,
        "review_archive_ttl_days": int,
        "new_problems_per_day": int,
    },
    "problem_solving": {
        "collection": str,
        "database_path": str,
        "log_path": str,
        "notes_directory": str,
        "supabase_url": str,
        "private_content_sync": bool,
        "retain_conversation_history": bool,
        "implementation_language": str,
    },
    "reviewer": {
        "provider": str,
        "model": str,
        "reasoning_effort": str,
        "service_tier": str,
        "follow_up_provider": str,
        "follow_up_model": str,
        "follow_up_reasoning_effort": str,
        "follow_up_service_tier": str,
    },
    "editor": {
        "indent_width": int,
        "which_key_delay_ms": int,
        "enhanced_syntax_highlighting": bool,
        "local_completion": bool,
    },
    "evaluation": {
        "compiler": str,
    },
    "sync": {
        "supabase_url": str,
    },
    "statusline": {
        "enabled": bool,
        "left": list,
        "right": list,
        "separator": str,
    },
}
STATUSLINE_ITEMS = {
    "exercise_name",
    "exercise_id",
    "collection",
    "phase",
    "phase_elapsed",
    "solve_elapsed",
    "language",
    "modified",
    "position",
    "compile_result",
    "proposed_rating",
    "progress",
    "action",
    "time_today",
    "reviews_today",
    "reviews_total",
    "due_now",
    "due_later_today",
    "new_today",
    "new_exercise",
    "new_left",
    "collection_progress",
    "tomorrow_due",
    "problem_name",
    "problem_id",
    "hint_requested",
    "outline_revealed",
    "bookmarked",
    "open_bookmarks",
    "conversation",
}
EFFORTS = {"minimal", "low", "medium", "high", "xhigh"}
REVIEWER_PROVIDERS = {"codex", "openai"}
SERVICE_TIERS = {"default", "fast", "flex"}
PATH_KEYS = {
    ("practice", "collection"),
    ("practice", "database_path"),
    ("practice", "log_path"),
    ("practice", "notes_directory"),
    ("problem_solving", "collection"),
    ("problem_solving", "database_path"),
    ("problem_solving", "log_path"),
    ("problem_solving", "notes_directory"),
}


def default_config_path() -> Path:
    root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "leetkatas" / "practice.toml"


def load_config(path: Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"could not read {path}: {error}") from error

    unknown_sections = sorted(set(value) - set(SCHEMA))
    if unknown_sections:
        raise ConfigError(f"unknown section: {unknown_sections[0]}")
    for section, fields in value.items():
        if not isinstance(fields, dict):
            raise ConfigError(f"{section} must be a table")
        unknown_fields = sorted(set(fields) - set(SCHEMA[section]))
        if unknown_fields:
            raise ConfigError(f"unknown setting: {section}.{unknown_fields[0]}")
        for name, item in fields.items():
            expected = SCHEMA[section][name]
            if type(item) is not expected or isinstance(item, str) and not item:
                raise ConfigError(f"{section}.{name} must be a non-empty {expected.__name__}")

    editor = value.get("editor", {})
    if "indent_width" in editor and not 1 <= editor["indent_width"] <= 16:
        raise ConfigError("editor.indent_width must be between 1 and 16")
    if "which_key_delay_ms" in editor and not 0 <= editor["which_key_delay_ms"] <= 5000:
        raise ConfigError("editor.which_key_delay_ms must be between 0 and 5000")
    reviewer = value.get("reviewer", {})
    for name in ("provider", "follow_up_provider"):
        if name in reviewer and reviewer[name] not in REVIEWER_PROVIDERS:
            raise ConfigError(f"reviewer.{name} must be codex or openai")
    if "reasoning_effort" in reviewer and reviewer["reasoning_effort"] not in EFFORTS:
        raise ConfigError("reviewer.reasoning_effort must be minimal, low, medium, high, or xhigh")
    if "follow_up_reasoning_effort" in reviewer and reviewer["follow_up_reasoning_effort"] not in EFFORTS:
        raise ConfigError(
            "reviewer.follow_up_reasoning_effort must be minimal, low, medium, high, or xhigh"
        )
    for name in ("service_tier", "follow_up_service_tier"):
        if name in reviewer and reviewer[name] not in SERVICE_TIERS:
            raise ConfigError(f"reviewer.{name} must be default, fast, or flex")
    practice = value.get("practice", {})
    if "collection" in practice and "collections" in practice:
        raise ConfigError("practice.collection and practice.collections cannot both be set")
    if "collections" in practice:
        collections = practice["collections"]
        if not collections or any(type(item) is not str or not item for item in collections):
            raise ConfigError("practice.collections must be a non-empty list of non-empty strings")
        resolved_collections = []
        for item in collections:
            configured = Path(item).expanduser()
            if not configured.is_absolute():
                configured = path.parent / configured
            resolved_collections.append(str(configured.resolve()))
        if len(set(resolved_collections)) != len(resolved_collections):
            raise ConfigError("practice.collections must not contain duplicate paths")
        practice["collections"] = resolved_collections
    if "review_archive_ttl_days" in practice and not 0 <= practice["review_archive_ttl_days"] <= 3650:
        raise ConfigError("practice.review_archive_ttl_days must be between 0 and 3650")
    if "new_problems_per_day" in practice and practice["new_problems_per_day"] < 0:
        raise ConfigError("practice.new_problems_per_day must be a non-negative integer")
    problem_solving = value.get("problem_solving", {})
    if (language := problem_solving.get("implementation_language")) is not None and language != "cpp":
        raise ConfigError("problem_solving.implementation_language currently supports only cpp")
    statusline = value.get("statusline", {})
    for side in ("left", "right"):
        if side not in statusline:
            continue
        items = statusline[side]
        if any(type(item) is not str or item not in STATUSLINE_ITEMS for item in items):
            raise ConfigError(
                f"statusline.{side} must contain only supported statusline item names"
            )

    for section, name in PATH_KEYS:
        if name in value.get(section, {}):
            configured = Path(value[section][name]).expanduser()
            if not configured.is_absolute():
                configured = path.parent / configured
            value[section][name] = str(configured.resolve())
    return value


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise ConfigError("request must be a JSON object")
        configured_path = request.get("path")
        if configured_path is not None and (not isinstance(configured_path, str) or not configured_path):
            raise ConfigError("path must be a non-empty string when provided")
        path = Path(configured_path).expanduser() if configured_path else default_config_path()
        json.dump({"path": str(path), "config": load_config(path)}, sys.stdout)
        sys.stdout.write("\n")
        return 0
    except (ConfigError, json.JSONDecodeError) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
