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
        "database_path": str,
        "log_path": str,
        "notes_directory": str,
    },
    "reviewer": {
        "model": str,
        "reasoning_effort": str,
    },
    "editor": {
        "indent_width": int,
        "which_key_delay_ms": int,
    },
    "evaluation": {
        "compiler": str,
    },
}
EFFORTS = {"minimal", "low", "medium", "high", "xhigh"}
PATH_KEYS = {
    ("practice", "collection"),
    ("practice", "database_path"),
    ("practice", "log_path"),
    ("practice", "notes_directory"),
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
    if "reasoning_effort" in reviewer and reviewer["reasoning_effort"] not in EFFORTS:
        raise ConfigError("reviewer.reasoning_effort must be minimal, low, medium, high, or xhigh")

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
