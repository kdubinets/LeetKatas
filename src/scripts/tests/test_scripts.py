from __future__ import annotations

import io
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import codex_reviewer  # noqa: E402
from codex_reviewer import SCHEMA, build_prompt  # noqa: E402
from evaluate_exercise import evaluate, parse_metadata_sections  # noqa: E402
from load_practice_config import ConfigError, load_config  # noqa: E402
from openai_reviewer import build_request, output_text, request_review  # noqa: E402
from record_rating import record_rating  # noqa: E402
from practice_scheduler import PracticeStore, deserialize_card  # noqa: E402
from practice_stats import practice_stats  # noqa: E402
from review_follow_up import ask  # noqa: E402
from reviewer_protocol import review_request  # noqa: E402
from select_exercise import select_exercise  # noqa: E402


def run_script(name: str, request: object) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(
        ["python3", str(SCRIPTS / name)],
        input=json.dumps(request),
        capture_output=True,
        check=False,
        text=True,
    )
    return result, json.loads(result.stdout)


class PracticeConfigTests(unittest.TestCase):
    def test_missing_config_uses_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(load_config(Path(temporary) / "missing.toml"), {})

    def test_loads_problem_solving_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "problem-solving.toml"
            path.write_text(
                """[problem_solving]
collection = "collections/seed"
database_path = "state.sqlite3"
log_path = "problem-solving.log"
notes_directory = "notes"
supabase_url = "https://example.supabase.co"
private_content_sync = true
retain_conversation_history = false
""",
                encoding="utf-8",
            )

            config = load_config(path)["problem_solving"]

            self.assertEqual(config["collection"], str((Path(temporary) / "collections/seed").resolve()))
            self.assertEqual(config["database_path"], str((Path(temporary) / "state.sqlite3").resolve()))
            self.assertEqual(config["log_path"], str((Path(temporary) / "problem-solving.log").resolve()))
            self.assertEqual(config["notes_directory"], str((Path(temporary) / "notes").resolve()))
            self.assertTrue(config["private_content_sync"])
            self.assertFalse(config["retain_conversation_history"])

    def test_loads_settings_and_resolves_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            path = directory / "practice.toml"
            path.write_text(
                """
[practice]
collection = "collections/core"
notes_directory = "notes"
review_archive_ttl_days = 45

[reviewer]
provider = "openai"
model = "gpt-5.6-luna"
reasoning_effort = "low"
follow_up_provider = "codex"
follow_up_model = "gpt-5.6-terra"
follow_up_reasoning_effort = "medium"

[editor]
indent_width = 2
which_key_delay_ms = 150
enhanced_syntax_highlighting = false
local_completion = true

[evaluation]
compiler = "g++"

[sync]
supabase_url = "https://example.supabase.co"

[statusline]
left = ["exercise_name"]
right = ["time_today", "due_now", "new_left"]
separator = " | "
""".strip()
            )

            config = load_config(path)

            self.assertEqual(config["practice"]["collection"], str(directory / "collections/core"))
            self.assertEqual(config["practice"]["notes_directory"], str(directory / "notes"))
            self.assertEqual(config["practice"]["review_archive_ttl_days"], 45)
            self.assertEqual(config["reviewer"]["model"], "gpt-5.6-luna")
            self.assertEqual(config["reviewer"]["provider"], "openai")
            self.assertEqual(config["reviewer"]["follow_up_provider"], "codex")
            self.assertEqual(config["reviewer"]["follow_up_model"], "gpt-5.6-terra")
            self.assertEqual(config["reviewer"]["follow_up_reasoning_effort"], "medium")
            self.assertEqual(config["editor"]["indent_width"], 2)
            self.assertFalse(config["editor"]["enhanced_syntax_highlighting"])
            self.assertTrue(config["editor"]["local_completion"])
            self.assertEqual(config["evaluation"]["compiler"], "g++")
            self.assertEqual(config["sync"]["supabase_url"], "https://example.supabase.co")
            self.assertEqual(config["statusline"]["left"], ["exercise_name"])
            self.assertEqual(
                config["statusline"]["right"], ["time_today", "due_now", "new_left"]
            )

    def test_rejects_unknown_or_invalid_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "practice.toml"
            path.write_text("[reviewer]\nreasoning_effort = \"extreme\"\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text('[practice]\ncollection = "core"\ncollections = ["chrono"]\n')
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text("[reviewer]\nfollow_up_reasoning_effort = \"extreme\"\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text("[reviewer]\nprovider = \"unknown\"\n")
            with self.assertRaisesRegex(ConfigError, "provider must be codex or openai"):
                load_config(path)

            path.write_text("[editor]\nunknown = 1\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text("[practice]\nreview_archive_ttl_days = 3651\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text('[statusline]\nleft = ["not_a_real_item"]\n')
            with self.assertRaises(ConfigError):
                load_config(path)

    def test_loads_multiple_collection_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "practice.toml"
            path.write_text('[practice]\ncollections = ["collections/core", "collections/chrono"]\n')
            config = load_config(path)
            self.assertEqual(config["practice"]["collections"], [
                str(root / "collections/core"), str(root / "collections/chrono"),
            ])


class SelectExerciseTests(unittest.TestCase):
    def create_pair(self, directory: Path, name: str) -> None:
        (directory / f"{name}.cpp").write_text("int solve() { return 1; }\n")
        (directory / f"{name}.md").write_text(f"# Name\n\n{name}\n")

    def write_order(self, directory: Path, exercise_ids: list[str]) -> None:
        (directory / "exercise_order.md").write_text("\n".join(exercise_ids) + "\n")

    def request(self, directory: Path, previous: str | None = None) -> dict:
        return {
            "exercise_directory": str(directory),
            "database_path": str(directory / "practice.sqlite3"),
            "source_extension": ".cpp",
            "metadata_extension": ".md",
            "previous_exercise_id": previous,
        }

    def test_selects_a_complete_pair_and_ignores_unpaired_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "complete")
            (directory / "unpaired.cpp").write_text("int value;\n")

            result, response = run_script("select_exercise.py", self.request(directory))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(response["exercise"]["id"], "complete")
            self.assertEqual(response["exercise"]["name"], "complete")
            self.assertTrue(Path(response["exercise"]["source_path"]).is_absolute())
            self.assertNotIn("target_environment", response["exercise"])

    def test_includes_optional_collection_target_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "complete")
            target_environment = {
                "language": {"name": "Python", "version": "3.12"},
                "libraries": [
                    {"name": "Python standard library", "version": "3.12"},
                    {"name": "itertools", "version": "standard library"},
                ],
            }
            (directory / "environment.json").write_text(
                json.dumps(target_environment)
            )

            result, response = run_script("select_exercise.py", self.request(directory))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                response["exercise"]["target_environment"], target_environment
            )

    def test_rejects_invalid_collection_target_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "complete")
            (directory / "environment.json").write_text('{"language": "C++"}')

            result, response = run_script("select_exercise.py", self.request(directory))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("target environment language", response["error"])

    def test_avoids_the_previous_exercise_when_an_alternative_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "first")
            self.create_pair(directory, "second")

            result, response = run_script(
                "select_exercise.py", self.request(directory, "first")
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(response["exercise"]["id"], "second")

    def test_allows_repeating_the_only_exercise(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "only")

            result, response = run_script(
                "select_exercise.py", self.request(directory, "only")
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(response["exercise"]["id"], "only")

    def test_selects_unseen_exercises_in_recommended_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for exercise_id in ("first", "second", "third"):
                self.create_pair(directory, exercise_id)
            self.write_order(directory, ["second", "third", "first"])

            result, response = run_script(
                "select_exercise.py", self.request(directory)
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(response["exercise"]["id"], "second")

    def test_skip_temporarily_bypasses_ordered_unseen_exercise(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "first")
            self.create_pair(directory, "second")
            self.write_order(directory, ["first", "second"])

            result, response = run_script(
                "select_exercise.py", self.request(directory, "first")
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(response["exercise"]["id"], "second")

    def test_rejects_an_incomplete_exercise_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "first")
            self.create_pair(directory, "missing")
            self.write_order(directory, ["first"])

            result, response = run_script(
                "select_exercise.py", self.request(directory)
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exercise order is missing", response["error"])

    def test_rejects_decorated_exercise_order_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "first")
            (directory / "exercise_order.md").write_text("1. `first`\n")

            result, response = run_script(
                "select_exercise.py", self.request(directory)
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid exercise ID", response["error"])

    def test_core_collection_starts_with_order_file_first_exercise(self) -> None:
        core = SCRIPTS.parents[1] / "practice" / "cpp" / "collections" / "core"
        with tempfile.TemporaryDirectory() as temporary:
            request = self.request(core)
            request["database_path"] = str(Path(temporary) / "practice.sqlite3")

            response = select_exercise(
                request, datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc)
            )

            self.assertEqual(response["exercise"]["id"], "fill_fixed_array")
            self.assertEqual(
                response["exercise"]["target_environment"]["language"],
                {"name": "C++", "version": "C++20"},
            )

    def test_reports_an_empty_collection_as_a_command_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, response = run_script(
                "select_exercise.py", self.request(Path(temporary))
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no .cpp/.md exercise pairs", response["error"])


class EvaluateExerciseTests(unittest.TestCase):
    def request(self, source: Path, metadata: Path) -> dict:
        return {
            "source_path": str(source),
            "metadata_path": str(metadata),
            "command": [
                "g++",
                "-std=c++20",
                "-Wall",
                "-Wextra",
                "-Werror",
                "-fsyntax-only",
                "{source}",
            ],
        }

    def test_successful_compilation_returns_metadata_and_good(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            source.write_text("int solve() { return 1; }\n")
            metadata.write_text("# Solution\n\n```cpp\nreturn 1;\n```\n")

            result, response = run_script(
                "evaluate_exercise.py", self.request(source, metadata)
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(response["compiled"])
            self.assertIsNone(response["proposed_rating"])
            self.assertEqual(response["review"]["status"], "unavailable")
            self.assertEqual(response["metadata"], metadata.read_text())
            self.assertEqual(response["metadata_sections"], [{
                "title": "Solution", "heading_line": 1, "blocks": [
                    {"type": "text", "start_line": 2, "lines": [""]},
                    {"type": "code", "language": "cpp", "start_line": 4,
                     "lines": ["return 1;"]},
                ],
            }])

    def test_failed_compilation_is_a_valid_fail_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "invalid.cpp"
            metadata = directory / "invalid.md"
            source.write_text("int solve(\n")
            metadata.write_text("# Solution\n")

            result, response = run_script(
                "evaluate_exercise.py", self.request(source, metadata)
            )

            self.assertEqual(result.returncode, 0)
            self.assertFalse(response["compiled"])
            self.assertIsNone(response["proposed_rating"])
            self.assertEqual(response["review"]["status"], "unavailable")
            self.assertIn("error:", response["diagnostics"])
            self.assertEqual(response["metadata"], metadata.read_text())

    def test_missing_command_placeholder_is_a_command_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            source.write_text("int value;\n")
            metadata.write_text("metadata\n")
            request = self.request(source, metadata)
            request["command"] = ["g++", "-fsyntax-only"]

            result, response = run_script("evaluate_exercise.py", request)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("{source} placeholder", response["error"])

    def test_reports_compiler_and_reviewer_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            progress = directory / "progress.jsonl"
            source.write_text("int solve() { return 1; }\n")
            metadata.write_text("# Solution\n")
            request = self.request(source, metadata)
            request["progress_path"] = str(progress)

            result, _ = run_script("evaluate_exercise.py", request)

            self.assertEqual(result.returncode, 0)
            events = [json.loads(line) for line in progress.read_text().splitlines()]
            self.assertEqual(
                [event["event"] for event in events],
                [
                    "compilation_started",
                    "compilation_finished",
                    "review_finished",
                    "evaluation_finished",
                ],
            )
            self.assertTrue(events[1]["compiled"])

    def test_passes_target_environment_as_language_neutral_review_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            source.write_text("int solve() { return 1; }\n")
            metadata.write_text("# Solution\n")
            request = self.request(source, metadata)
            request["target_environment"] = {
                "language": {"name": "C++", "version": "C++20"}
            }
            request["reviewer"] = {"command": ["fake-reviewer"]}
            review = {
                "status": "available",
                "attempts": 1,
                "feedback": {"proposed_rating": "good"},
                "failure": None,
            }

            with patch("evaluate_exercise.review_request", return_value=review) as reviewer:
                response = evaluate(request)

            evidence = reviewer.call_args.args[0]
            self.assertEqual(
                evidence["target_environment"], request["target_environment"]
            )
            self.assertEqual(evidence["exercise_metadata"], "# Solution\n")
            self.assertTrue(evidence["validation"]["succeeded"])
            self.assertNotIn("compiler", evidence)
            self.assertEqual(response["proposed_rating"], "good")

    def test_reports_configured_reviewer_model_and_effort(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            source.write_text("int solve() { return 1; }\n")
            metadata.write_text("# Solution\n")
            request = self.request(source, metadata)
            request["reviewer"] = {
                "command": ["fake-reviewer"],
                "name": "Codex",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "low",
            }
            review = {
                "status": "available",
                "attempts": 1,
                "feedback": {"proposed_rating": "good"},
                "failure": None,
            }

            with patch("evaluate_exercise.review_request", return_value=review):
                response = evaluate(request)

            self.assertEqual(response["review"]["model"], "gpt-5.6-luna")
            self.assertEqual(response["review"]["reasoning_effort"], "low")

    def test_rejects_invalid_target_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "valid.cpp"
            metadata = directory / "valid.md"
            source.write_text("int solve() { return 1; }\n")
            metadata.write_text("# Solution\n")
            request = self.request(source, metadata)
            request["target_environment"] = {
                "language": {"name": "C++", "version": ""}
            }

            result, response = run_script("evaluate_exercise.py", request)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("language.version", response["error"])


class CodexReviewerTests(unittest.TestCase):
    def test_strict_schema_requires_every_declared_property(self) -> None:
        self.assertEqual(set(SCHEMA["properties"]), set(SCHEMA["required"]))
        self.assertIn("null", SCHEMA["properties"]["version_notes"]["type"])

    def test_builds_prompt_from_adapter_specific_file_and_appends_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            prompt_path = Path(temporary) / "reviewer.txt"
            prompt_path.write_text("Adapter-specific instructions.\n")
            evidence = {"submitted_source": "answer()"}

            with patch("codex_reviewer.PROMPT_PATH", prompt_path):
                prompt = build_prompt(evidence)

            self.assertTrue(prompt.startswith("Adapter-specific instructions.\n\n"))
            encoded_evidence = prompt.split("Review evidence:\n", 1)[1]
            self.assertEqual(json.loads(encoded_evidence), evidence)

    def test_default_prompt_contains_rating_and_validation_calibration(self) -> None:
        prompt = build_prompt({})

        self.assertIn("failed validation does not automatically require `fail`", prompt)
        self.assertIn("target environment", prompt)
        self.assertIn("recall difficulty and confidence", prompt)
        self.assertIn("provide a corrected implementation", prompt)
        self.assertIn("untrusted reference candidate, not as a gold standard", prompt)
        self.assertIn("look for at most one meaningful opportunity", prompt)
        self.assertIn("one or two learner-facing plain-text sentences", prompt)
        self.assertIn("Optionally provide `version_notes`", prompt)
        self.assertIn("must not affect the verdict, proposed rating", prompt)

    def test_follow_up_prompt_uses_separate_instructions(self) -> None:
        prompt = build_prompt({"question": "Why?"}, follow_up=True)

        self.assertIn("learner's follow-up question", prompt)
        self.assertIn("do not emit a replacement verdict or rating", prompt)
        self.assertEqual(
            json.loads(prompt.split("Follow-up context:\n", 1)[1]),
            {"question": "Why?"},
        )

    def test_always_ignores_user_config(self) -> None:
        commands: list[list[str]] = []

        def run(command, **unused):
            commands.append(command)
            output = Path(command[command.index("--output-last-message") + 1])
            output.write_text("{}", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        stdout = io.StringIO()
        with (
            patch.object(sys, "argv", ["codex_reviewer.py"]),
            patch.object(sys, "stdin", io.StringIO("{}")),
            patch.object(sys, "stdout", stdout),
            patch("codex_reviewer.subprocess.run", side_effect=run),
        ):
            returncode = codex_reviewer.main()

        self.assertEqual(returncode, 0)
        self.assertIn("--ignore-user-config", commands[0])
        self.assertNotIn("--json", commands[0])
        self.assertEqual(json.loads(stdout.getvalue()), {})


class OpenAIReviewerTests(unittest.TestCase):
    def test_builds_a_stateless_strict_structured_response_request(self) -> None:
        evidence = {"submitted_source": "return 42;"}

        request = build_request(evidence, "gpt-5.6-luna", "low", follow_up=False)

        self.assertFalse(request["store"])
        self.assertEqual(request["model"], "gpt-5.6-luna")
        self.assertEqual(request["reasoning"], {"effort": "low"})
        self.assertEqual(json.loads(request["input"].split("Review evidence:\n", 1)[1]), evidence)
        self.assertIn("failed validation", request["instructions"])
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(request["text"]["format"]["schema"], SCHEMA)

    def test_extracts_text_from_a_responses_api_output_item(self) -> None:
        response = {"output": [{"content": [{"type": "output_text", "text": "{\"answer\": \"Yes\"}"}]}]}

        self.assertEqual(output_text(response), '{"answer": "Yes"}')

    def test_posts_the_request_and_parses_the_structured_output(self) -> None:
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *unused):
                return False

            def read(self):
                return b'{"output_text":"{\\"answer\\":\\"Yes\\"}"}'

        body = build_request({"question": "Why?"}, "gpt-5.6-luna", None, follow_up=True)
        with patch("openai_reviewer.urlopen", return_value=FakeResponse()) as send:
            review = request_review(body, "test-api-key")

        outgoing = send.call_args.args[0]
        self.assertEqual(outgoing.full_url, "https://api.openai.com/v1/responses")
        self.assertEqual(outgoing.get_header("Authorization"), "Bearer test-api-key")
        self.assertEqual(json.loads(outgoing.data.decode("utf-8")), body)
        self.assertEqual(review, {"answer": "Yes"})


class ReviewerProtocolTests(unittest.TestCase):
    def test_reports_safe_http_category_for_each_failed_attempt(self) -> None:
        progress: list[dict] = []
        failed = subprocess.CompletedProcess(["reviewer"], 1, stdout="", stderr="OpenAI API request failed with HTTP 403")

        with patch("reviewer_protocol.subprocess.run", return_value=failed), patch("reviewer_protocol.time.sleep"):
            result = review_request({}, ["reviewer"], progress=lambda event, **details: progress.append({"event": event, **details}))

        self.assertEqual(result["status"], "unavailable")
        failed_events = [event for event in progress if event["event"] == "review_attempt_failed"]
        self.assertEqual([event["failure_category"] for event in failed_events], ["http_403"] * 3)


class FollowUpReviewTests(unittest.TestCase):
    def test_uses_separate_reviewer_model_and_returns_answer(self) -> None:
        request = {
            "evidence": {"submitted_source": "return 42;"},
            "initial_review": {"status": "available", "feedback": {}},
            "messages": [],
            "question": "Why is this correct?",
            "reviewer": {
                "command": ["fake-follow-up"],
                "name": "Tutor",
                "model": "follow-up-model",
                "reasoning_effort": "medium",
            },
        }
        follow_up = {
            "status": "available",
            "attempts": 1,
            "answer": "Because it returns the requested value.",
            "failure": None,
        }

        with patch("review_follow_up.follow_up_request", return_value=follow_up) as reviewer:
            response = ask(request)

        self.assertEqual(reviewer.call_args.args[0]["question"], request["question"])
        self.assertEqual(response["answer"], follow_up["answer"])
        self.assertEqual(response["reviewer"], "Tutor")
        self.assertEqual(response["model"], "follow-up-model")
        self.assertEqual(response["reasoning_effort"], "medium")

    def test_rejects_excessive_conversation_history(self) -> None:
        request = {
            "evidence": {},
            "initial_review": {},
            "messages": [
                {"role": "user", "content": "question"}
                for _ in range(17)
            ],
            "question": "Why?",
            "reviewer": {"command": ["fake-follow-up"]},
        }

        with self.assertRaisesRegex(ValueError, "at most 16"):
            ask(request)


class MetadataSectionTests(unittest.TestCase):
    def test_preserves_sections_text_code_language_and_source_lines(self) -> None:
        metadata = """Preamble
# Name

Example

# Solution
Use this:

```cpp
return 42;
```
# Notes
Unknown section.
"""
        self.assertEqual(parse_metadata_sections(metadata), [
            {"title": "Name", "heading_line": 2, "blocks": [
                {"type": "text", "start_line": 3, "lines": ["", "Example", ""]},
            ]},
            {"title": "Solution", "heading_line": 6, "blocks": [
                {"type": "text", "start_line": 7, "lines": ["Use this:", ""]},
                {"type": "code", "language": "cpp", "start_line": 10,
                 "lines": ["return 42;"]},
            ]},
            {"title": "Notes", "heading_line": 12, "blocks": [
                {"type": "text", "start_line": 13, "lines": ["Unknown section."]},
            ]},
        ])

    def test_handles_blank_sections_and_fences_without_languages(self) -> None:
        self.assertEqual(parse_metadata_sections("# Empty\n# Code\n```\nx();\n```\n"), [
            {"title": "Empty", "heading_line": 1, "blocks": []},
            {"title": "Code", "heading_line": 2, "blocks": [
                {"type": "code", "language": "", "start_line": 4,
                 "lines": ["x();"]},
            ]},
        ])

    def test_returns_no_sections_without_level_one_headings(self) -> None:
        self.assertEqual(parse_metadata_sections("legacy metadata\n```cpp\nx();\n```\n"), [])

    def test_keeps_unclosed_fence_as_partial_code(self) -> None:
        self.assertEqual(parse_metadata_sections("# Solution\n```cpp\nx();\n# not a heading\n"), [{
            "title": "Solution", "heading_line": 1, "blocks": [
                {"type": "code", "language": "cpp", "start_line": 3,
                 "lines": ["x();", "# not a heading"]},
            ],
        }])


class RecordRatingTests(unittest.TestCase):
    def create_pair(self, directory: Path, name: str) -> None:
        (directory / f"{name}.cpp").write_text("int solve() { return 1; }\n")
        (directory / f"{name}.md").write_text(f"# Name\n\n{name}\n")

    def request(self, directory: Path, final_rating: str) -> dict:
        return {
            "exercise_directory": str(directory),
            "database_path": str(directory / "practice.sqlite3"),
            "exercise_id": "example",
            "compiled": True,
            "proposed_rating": "good",
            "final_rating": final_rating,
        }

    def test_persists_a_valid_override(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "example")
            result, response = run_script(
                "record_rating.py", self.request(directory, "excellent")
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(response["recorded"])
            self.assertIsInstance(response["due"], str)
            self.assertEqual(response["state"], "review")

            with sqlite3.connect(directory / "practice.sqlite3") as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM cards").fetchone()[0], 1)
                review_count = connection.execute("SELECT count(*) FROM reviews").fetchone()[0]
                self.assertEqual(review_count, 1)

            selection_request = {
                "exercise_directory": str(directory),
                "database_path": str(directory / "practice.sqlite3"),
                "source_extension": ".cpp",
                "metadata_extension": ".md",
                "previous_exercise_id": "example",
            }
            selected_result, selected_response = run_script(
                "select_exercise.py", selection_request
            )
            self.assertEqual(selected_result.returncode, 0)
            self.assertIsNone(selected_response["exercise"])
            self.assertEqual(selected_response["next_due"], response["due"])

    def test_persists_reviewer_model_and_reasoning_effort(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "example")
            request = self.request(directory, "good")
            request.update(
                reviewer_model="gpt-5.6-luna",
                reviewer_reasoning_effort="low",
            )

            result, _ = run_script("record_rating.py", request)

            self.assertEqual(result.returncode, 0)
            with sqlite3.connect(directory / "practice.sqlite3") as connection:
                stored = connection.execute(
                    "SELECT reviewer_model, reviewer_reasoning_effort FROM reviews"
                ).fetchone()
            self.assertEqual(stored, ("gpt-5.6-luna", "low"))

    def test_persists_practice_durations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "example")
            request = self.request(directory, "good")
            request.update(solve_duration_ms=1250, feedback_duration_ms=750)

            result, _ = run_script("record_rating.py", request)

            self.assertEqual(result.returncode, 0)
            with sqlite3.connect(directory / "practice.sqlite3") as connection:
                stored = connection.execute(
                    "SELECT solve_duration_ms, feedback_duration_ms FROM reviews"
                ).fetchone()
            self.assertEqual(stored, (1250, 750))

    def test_rejects_incomplete_or_negative_practice_durations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "example")
            incomplete = self.request(directory, "good")
            incomplete["solve_duration_ms"] = 10
            result, response = run_script("record_rating.py", incomplete)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be provided together", response["error"])

            negative = self.request(directory, "good")
            negative.update(solve_duration_ms=-1, feedback_duration_ms=10)
            result, response = run_script("record_rating.py", negative)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-negative", response["error"])

    def test_archives_submission_and_full_review_with_ttl(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            self.create_pair(directory, "example")
            request = self.request(directory, "good")
            request.update(
                submitted_source="int solve() { return 2; }\n",
                review_response={
                    "status": "available",
                    "feedback": {"summary": "Correct, with a clearer alternative."},
                },
                review_archive_ttl_days=7,
            )
            reviewed_at = datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc)

            record_rating(request, reviewed_at)

            with sqlite3.connect(database) as connection:
                stored = connection.execute(
                    """SELECT created_at, expires_at, submitted_source,
                              review_response_json
                       FROM review_artifacts"""
                ).fetchone()
            self.assertEqual(stored[0], reviewed_at.isoformat())
            self.assertEqual(
                stored[1], (reviewed_at + timedelta(days=7)).isoformat()
            )
            self.assertEqual(stored[2], request["submitted_source"])
            self.assertEqual(json.loads(stored[3]), request["review_response"])
            self.assertEqual(database.stat().st_mode & 0o777, 0o600)

    def test_purges_expired_artifacts_when_recording_a_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            self.create_pair(directory, "example")
            self.create_pair(directory, "later")
            first = self.request(directory, "good")
            first.update(
                submitted_source="first submission",
                review_response={"status": "available", "feedback": {}},
                review_archive_ttl_days=1,
            )
            reviewed_at = datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc)
            record_rating(first, reviewed_at)

            later = self.request(directory, "good")
            later.update(
                exercise_id="later",
                submitted_source="later submission",
                review_response={"status": "available", "feedback": {}},
                review_archive_ttl_days=30,
            )
            record_rating(later, reviewed_at + timedelta(days=2))

            with sqlite3.connect(database) as connection:
                sources = connection.execute(
                    "SELECT submitted_source FROM review_artifacts"
                ).fetchall()
            self.assertEqual(sources, [("later submission",)])

    def test_zero_ttl_disables_artifact_archiving(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "example")
            request = self.request(directory, "good")
            request.update(
                submitted_source="submission",
                review_response={"status": "available", "feedback": {}},
                review_archive_ttl_days=0,
            )

            result, _ = run_script("record_rating.py", request)

            self.assertEqual(result.returncode, 0)
            with sqlite3.connect(directory / "practice.sqlite3") as connection:
                count = connection.execute(
                    "SELECT count(*) FROM review_artifacts"
                ).fetchone()[0]
            self.assertEqual(count, 0)

    def test_rejects_an_invalid_rating(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, response = run_script(
                "record_rating.py", self.request(Path(temporary), "perfect")
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("final_rating", response["error"])


class PracticeStatsTests(unittest.TestCase):
    NOW = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)
    LOCAL_ZONE = ZoneInfo("Europe/Dublin")

    def create_pair(self, directory: Path, name: str) -> None:
        (directory / f"{name}.cpp").write_text("int solve() { return 1; }\n")
        (directory / f"{name}.md").write_text(f"# Name\n\n{name}\n")

    def request(self, directory: Path) -> dict:
        return {
            "exercise_directory": str(directory),
            "database_path": str(directory / "practice.sqlite3"),
            "source_extension": ".cpp",
            "metadata_extension": ".md",
            "history_days": 30,
        }

    def record(
        self,
        directory: Path,
        exercise_id: str,
        rating: str,
        reviewed_at: datetime,
        solve_ms: int | None = None,
        feedback_ms: int | None = None,
    ) -> None:
        record_rating(
            {
                "exercise_directory": str(directory),
                "database_path": str(directory / "practice.sqlite3"),
                "exercise_id": exercise_id,
                "compiled": rating != "fail",
                "proposed_rating": rating,
                "final_rating": rating,
                "solve_duration_ms": solve_ms,
                "feedback_duration_ms": feedback_ms,
            },
            reviewed_at,
        )

    def set_due(self, directory: Path, exercise_id: str, due: datetime) -> None:
        database = directory / "practice.sqlite3"
        collection = str(directory.resolve())
        with sqlite3.connect(database) as connection:
            serialized = connection.execute(
                "SELECT card_json FROM cards WHERE collection_key = ? AND exercise_id = ?",
                (collection, exercise_id),
            ).fetchone()[0]
            card = deserialize_card(serialized)
            card.due = due
            connection.execute(
                "UPDATE cards SET card_json = ?, due_at = ? WHERE collection_key = ? AND exercise_id = ?",
                (card.to_json(), due.isoformat(), collection, exercise_id),
            )

    def test_reports_today_collection_forecast_and_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for exercise_id in ("learned", "learning", "tomorrow", "unseen"):
                self.create_pair(directory, exercise_id)

            self.record(directory, "learned", "excellent", self.NOW - timedelta(days=1))
            self.record(directory, "learned", "good", self.NOW, 1000, 500)
            self.record(directory, "learning", "fail", self.NOW + timedelta(minutes=1))
            self.record(directory, "tomorrow", "excellent", self.NOW + timedelta(minutes=2), 2000, 1000)
            self.set_due(directory, "learned", self.NOW - timedelta(hours=1))
            self.set_due(directory, "learning", self.NOW + timedelta(hours=3))
            self.set_due(directory, "tomorrow", self.NOW + timedelta(days=1))

            result = practice_stats(self.request(directory), self.NOW, self.LOCAL_ZONE)

            self.assertEqual(result["today"]["reviews"], 3)
            self.assertEqual(result["today"]["new_introduced"], 2)
            self.assertEqual(result["today"]["due_now"], 1)
            self.assertEqual(result["today"]["due_later_today"], 1)
            self.assertEqual(result["today"]["ratings"], {
                "fail": 1, "acceptable": 0, "good": 1, "excellent": 1,
            })
            self.assertEqual(result["today"]["practice_time_ms"], 4500)
            self.assertEqual(result["today"]["tracked_reviews"], 2)
            self.assertEqual(result["collection_state"]["total"], 4)
            self.assertEqual(result["collection_state"]["unseen"], 1)
            self.assertEqual(result["collection_state"]["learning"], 1)
            self.assertEqual(result["collection_state"]["learned"], 2)
            self.assertEqual(result["forecast"]["tomorrow_due"], 1)
            self.assertEqual(len(result["history"]), 30)
            self.assertEqual(result["history"][0]["date"], "2026-06-15")
            self.assertEqual(result["history"][1]["date"], "2026-06-14")

    def test_uses_local_calendar_dates_across_dst(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "boundary")
            reviewed_at = datetime(2026, 3, 29, 23, 30, tzinfo=timezone.utc)
            self.record(directory, "boundary", "good", reviewed_at, 10, 20)

            result = practice_stats(
                self.request(directory),
                datetime(2026, 3, 30, 12, 0, tzinfo=timezone.utc),
                self.LOCAL_ZONE,
            )

            self.assertEqual(result["today"]["date"], "2026-03-30")
            self.assertEqual(result["today"]["reviews"], 1)

    def test_aggregates_portfolio_statistics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, second = root / "first", root / "second"
            first.mkdir()
            second.mkdir()
            self.create_pair(first, "one")
            self.create_pair(second, "two")
            request = self.request(first)
            request.pop("exercise_directory")
            request["exercise_directories"] = [str(first), str(second)]
            result = practice_stats(request, self.NOW, self.LOCAL_ZONE)
            self.assertEqual(result["collection"], "portfolio")
            self.assertEqual(len(result["collections"]), 2)
            self.assertEqual(result["collection_state"]["total"], 2)
            self.assertEqual(result["collection_state"]["unseen"], 2)

    def test_migrates_v4_duration_columns_as_untracked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            with sqlite3.connect(database) as connection:
                connection.executescript(
                    """
                    CREATE TABLE schema_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    INSERT INTO schema_metadata VALUES ('schema_version', '4');
                    CREATE TABLE cards (
                      collection_key TEXT NOT NULL, exercise_id TEXT NOT NULL,
                      card_json TEXT NOT NULL, due_at TEXT NOT NULL,
                      created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                      PRIMARY KEY (collection_key, exercise_id));
                    CREATE TABLE reviews (
                      review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      collection_key TEXT NOT NULL, exercise_id TEXT NOT NULL,
                      review_datetime TEXT NOT NULL, final_rating TEXT NOT NULL,
                      compiled INTEGER NOT NULL, proposed_rating TEXT,
                      review_status TEXT NOT NULL DEFAULT 'legacy', reviewer_name TEXT,
                      reviewer_model TEXT, reviewer_reasoning_effort TEXT,
                      review_attempts INTEGER NOT NULL DEFAULT 0,
                      review_log_json TEXT NOT NULL,
                      FOREIGN KEY (collection_key, exercise_id)
                        REFERENCES cards (collection_key, exercise_id));
                    """
                )

            connection = PracticeStore(database).connect()
            try:
                columns = {row[1] for row in connection.execute("PRAGMA table_info(reviews)")}
                version = connection.execute(
                    "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertIn("solve_duration_ms", columns)
            self.assertIn("feedback_duration_ms", columns)
            self.assertEqual(version, "7")


class SchedulerIntegrationTests(unittest.TestCase):
    NOW = datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc)

    def create_pair(self, directory: Path, name: str) -> None:
        (directory / f"{name}.cpp").write_text("int solve() { return 1; }\n")
        (directory / f"{name}.md").write_text(f"# Name\n\n{name}\n")

    def write_order(self, directory: Path, exercise_ids: list[str]) -> None:
        (directory / "exercise_order.md").write_text("\n".join(exercise_ids) + "\n")

    def select_request(self, directory: Path, database: Path) -> dict:
        return {
            "exercise_directory": str(directory),
            "database_path": str(database),
            "source_extension": ".cpp",
            "metadata_extension": ".md",
            "previous_exercise_id": None,
        }

    def record_request(
        self, directory: Path, database: Path, exercise_id: str, rating: str
    ) -> dict:
        return {
            "exercise_directory": str(directory),
            "database_path": str(database),
            "exercise_id": exercise_id,
            "compiled": rating != "fail",
            "proposed_rating": "good" if rating != "fail" else "fail",
            "final_rating": rating,
        }

    def test_maps_all_ratings_and_keeps_immutable_review_logs(self) -> None:
        expected = {"fail": 1, "acceptable": 2, "good": 3, "excellent": 4}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            for index, rating in enumerate(expected):
                exercise_id = f"exercise_{index}"
                self.create_pair(directory, exercise_id)
                record_rating(
                    self.record_request(directory, database, exercise_id, rating),
                    self.NOW,
                )

            with sqlite3.connect(database) as connection:
                rows = connection.execute(
                    "SELECT final_rating, review_log_json FROM reviews ORDER BY review_id"
                ).fetchall()
            self.assertEqual(len(rows), 4)
            for final_rating, review_log_json in rows:
                self.assertEqual(json.loads(review_log_json)["rating"], expected[final_rating])

    def test_oldest_due_review_precedes_unseen_exercises(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            for exercise_id in ("oldest", "later", "unseen"):
                self.create_pair(directory, exercise_id)
            self.write_order(directory, ["unseen", "later", "oldest"])
            record_rating(
                self.record_request(directory, database, "oldest", "fail"), self.NOW
            )
            record_rating(
                self.record_request(directory, database, "later", "fail"),
                self.NOW + timedelta(seconds=30),
            )

            response = select_exercise(
                {
                    **self.select_request(directory, database),
                    "previous_exercise_id": "oldest",
                },
                self.NOW + timedelta(minutes=2),
            )

            self.assertEqual(response["exercise"]["id"], "oldest")

    def test_returns_unseen_before_a_future_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            self.create_pair(directory, "reviewed")
            self.create_pair(directory, "unseen")
            record_rating(
                self.record_request(directory, database, "reviewed", "good"), self.NOW
            )

            response = select_exercise(
                self.select_request(directory, database), self.NOW
            )

            self.assertEqual(response["exercise"]["id"], "unseen")

    def test_returns_next_due_when_collection_is_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            self.create_pair(directory, "only")
            recorded = record_rating(
                self.record_request(directory, database, "only", "good"), self.NOW
            )

            response = select_exercise(
                self.select_request(directory, database), self.NOW
            )

            self.assertIsNone(response["exercise"])
            self.assertEqual(response["next_due"], recorded["due"])

    def test_same_exercise_id_is_isolated_by_collection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            first.mkdir()
            second.mkdir()
            database = root / "practice.sqlite3"
            self.create_pair(first, "shared")
            self.create_pair(second, "shared")
            record_rating(
                self.record_request(first, database, "shared", "good"), self.NOW
            )

            response = select_exercise(self.select_request(second, database), self.NOW)

            self.assertEqual(response["exercise"]["id"], "shared")

    def test_portfolio_selects_oldest_due_and_balances_unseen_introductions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, second = root / "first", root / "second"
            first.mkdir()
            second.mkdir()
            database = root / "practice.sqlite3"
            self.create_pair(first, "first")
            self.create_pair(second, "second")
            request = {
                "exercise_directories": [str(first), str(second)],
                "database_path": str(database),
                "source_extension": ".cpp", "metadata_extension": ".md",
            }
            response = select_exercise(request, self.NOW)
            self.assertEqual(response["exercise"]["collection_directory"], str(first.resolve()))
            record_rating(self.record_request(first, database, "first", "fail"), self.NOW)
            response = select_exercise(request, self.NOW + timedelta(minutes=2))
            self.assertEqual(response["exercise"]["collection_directory"], str(first.resolve()))

    def test_failed_review_transaction_does_not_create_a_card(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            database = directory / "practice.sqlite3"
            self.create_pair(directory, "only")
            select_exercise(self.select_request(directory, database), self.NOW)
            with sqlite3.connect(database) as connection:
                connection.execute(
                    """
                    CREATE TRIGGER reject_reviews BEFORE INSERT ON reviews
                    BEGIN SELECT RAISE(ABORT, 'review rejected'); END
                    """
                )

            with self.assertRaises(sqlite3.DatabaseError):
                record_rating(
                    self.record_request(directory, database, "only", "good"), self.NOW
                )

            with sqlite3.connect(database) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM cards").fetchone()[0], 0)
                review_count = connection.execute("SELECT count(*) FROM reviews").fetchone()[0]
                self.assertEqual(review_count, 0)

    def test_corrupt_database_is_a_json_command_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "only")
            database = directory / "practice.sqlite3"
            database.write_bytes(b"not sqlite")

            result, response = run_script(
                "select_exercise.py", self.select_request(directory, database)
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("could not open practice database", response["error"])

    def test_unopenable_database_path_is_a_json_command_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.create_pair(directory, "only")
            request = self.select_request(directory, directory)

            result, response = run_script("select_exercise.py", request)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("could not open practice database", response["error"])


if __name__ == "__main__":
    unittest.main()
