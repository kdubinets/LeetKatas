#!/usr/bin/env python3
"""OpenAI Responses API reviewer implementing the generic reviewer contract."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from reviewer_assets import FOLLOW_UP_SCHEMA, SCHEMA, load_instructions

API_URL = "https://api.openai.com/v1/responses"
REQUEST_TIMEOUT_SECONDS = 50


class OpenAIReviewerError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--follow-up", action="store_true")
    parser.add_argument("--model", required=False)
    parser.add_argument("--effort", choices=("minimal", "low", "medium", "high", "xhigh"))
    return parser.parse_args()


def response_format(schema: dict[str, Any], follow_up: bool) -> dict[str, Any]:
    return {
        "type": "json_schema",
        "name": "practice_follow_up" if follow_up else "practice_review",
        "strict": True,
        "schema": schema,
    }


def build_request(
    evidence: dict[str, Any], model: str, effort: str | None, follow_up: bool
) -> dict[str, Any]:
    label = "Follow-up context" if follow_up else "Review evidence"
    body: dict[str, Any] = {
        "model": model,
        "instructions": load_instructions(follow_up=follow_up),
        "input": f"{label}:\n" + json.dumps(evidence),
        "store": False,
        "text": {"format": response_format(FOLLOW_UP_SCHEMA if follow_up else SCHEMA, follow_up)},
    }
    if effort:
        body["reasoning"] = {"effort": effort}
    return body


def output_text(response: dict[str, Any]) -> str:
    text = response.get("output_text")
    if isinstance(text, str) and text:
        return text
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str):
                    return text
            if isinstance(content, dict) and content.get("type") == "refusal":
                raise OpenAIReviewerError("OpenAI refused the reviewer request")
    raise OpenAIReviewerError("OpenAI returned no structured reviewer output")


def request_review(body: dict[str, Any], api_key: str) -> dict[str, Any]:
    encoded = json.dumps(body).encode("utf-8")
    request = Request(
        API_URL,
        data=encoded,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            value = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise OpenAIReviewerError(f"OpenAI API request failed with HTTP {error.code}") from error
    except URLError as error:
        raise OpenAIReviewerError("OpenAI API request could not be completed") from error
    except TimeoutError as error:
        raise OpenAIReviewerError("OpenAI API request timed out") from error
    except json.JSONDecodeError as error:
        raise OpenAIReviewerError("OpenAI API returned malformed JSON") from error
    if not isinstance(value, dict):
        raise OpenAIReviewerError("OpenAI API returned an invalid response")
    try:
        return json.loads(output_text(value))
    except json.JSONDecodeError as error:
        raise OpenAIReviewerError("OpenAI returned malformed structured output") from error


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if args.check:
        if api_key:
            return 0
        sys.stderr.write("OPENAI_API_KEY is not configured\n")
        return 1
    if not api_key:
        sys.stderr.write("OPENAI_API_KEY is not configured\n")
        return 1
    if not args.model:
        sys.stderr.write("--model is required\n")
        return 2
    try:
        evidence = json.load(sys.stdin)
        if not isinstance(evidence, dict):
            raise OpenAIReviewerError("reviewer input must be a JSON object")
        review = request_review(build_request(evidence, args.model, args.effort, args.follow_up), api_key)
    except (OpenAIReviewerError, json.JSONDecodeError) as error:
        sys.stderr.write(f"{error}\n")
        return 1
    json.dump(review, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
