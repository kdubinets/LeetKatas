#!/usr/bin/env python3
"""Discuss a revealed Level C solution outline."""

from __future__ import annotations

import json
import sqlite3
import sys

from level_c_conversation import discuss
from level_c_conversation_protocol import ConversationError
from practice_scheduler import SchedulerError


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise ConversationError("request must be a JSON object")
        response = discuss(request)
    except (
        ConversationError,
        SchedulerError,
        json.JSONDecodeError,
        OSError,
        UnicodeError,
        sqlite3.Error,
    ) as error:
        json.dump({"error": str(error)}, sys.stdout)
        sys.stdout.write("\n")
        return 1
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
