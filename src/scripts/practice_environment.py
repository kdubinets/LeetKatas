"""Collection-level target environment metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ENVIRONMENT_FILENAME = "environment.json"


class TargetEnvironmentError(ValueError):
    """Raised when collection target environment metadata is invalid."""


def _optional_string(value: Any, field: str) -> None:
    if value is not None and (not isinstance(value, str) or not value):
        raise TargetEnvironmentError(f"{field} must be a non-empty string or null")


def validate_target_environment(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TargetEnvironmentError("target environment must be an object")

    language = value.get("language")
    if not isinstance(language, dict):
        raise TargetEnvironmentError("target environment language must be an object")
    for field in ("name", "version"):
        if not isinstance(language.get(field), str) or not language[field]:
            raise TargetEnvironmentError(
                f"target environment language.{field} must be a non-empty string"
            )

    implementation = value.get("implementation")
    if implementation is not None:
        if not isinstance(implementation, dict):
            raise TargetEnvironmentError(
                "target environment implementation must be an object or null"
            )
        if (
            not isinstance(implementation.get("name"), str)
            or not implementation["name"]
        ):
            raise TargetEnvironmentError(
                "target environment implementation.name must be a non-empty string"
            )
        _optional_string(
            implementation.get("version"), "target environment implementation.version"
        )

    libraries = value.get("libraries", [])
    if not isinstance(libraries, list):
        raise TargetEnvironmentError("target environment libraries must be an array")
    for index, library in enumerate(libraries):
        if not isinstance(library, dict):
            raise TargetEnvironmentError(
                f"target environment libraries[{index}] must be an object"
            )
        if not isinstance(library.get("name"), str) or not library["name"]:
            raise TargetEnvironmentError(
                f"target environment libraries[{index}].name must be a non-empty string"
            )
        _optional_string(
            library.get("version"),
            f"target environment libraries[{index}].version",
        )

    restrictions = value.get("restrictions", [])
    if not isinstance(restrictions, list) or any(
        not isinstance(restriction, str) or not restriction
        for restriction in restrictions
    ):
        raise TargetEnvironmentError(
            "target environment restrictions must be an array of non-empty strings"
        )

    return value


def load_collection_environment(collection: Path) -> dict[str, Any] | None:
    path = collection / ENVIRONMENT_FILENAME
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise TargetEnvironmentError(
            f"invalid target environment JSON in {path}: {error.msg}"
        ) from error
    return validate_target_environment(value)
