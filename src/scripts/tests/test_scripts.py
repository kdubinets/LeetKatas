from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from codex_reviewer import build_prompt  # noqa: E402
from evaluate_exercise import evaluate  # noqa: E402
from load_practice_config import ConfigError, load_config  # noqa: E402
from record_rating import record_rating  # noqa: E402
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
model = "gpt-5.6-luna"
reasoning_effort = "low"

[editor]
indent_width = 2
which_key_delay_ms = 150

[evaluation]
compiler = "g++"
""".strip()
            )

            config = load_config(path)

            self.assertEqual(config["practice"]["collection"], str(directory / "collections/core"))
            self.assertEqual(config["practice"]["notes_directory"], str(directory / "notes"))
            self.assertEqual(config["practice"]["review_archive_ttl_days"], 45)
            self.assertEqual(config["reviewer"]["model"], "gpt-5.6-luna")
            self.assertEqual(config["editor"]["indent_width"], 2)
            self.assertEqual(config["evaluation"]["compiler"], "g++")

    def test_rejects_unknown_or_invalid_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "practice.toml"
            path.write_text("[reviewer]\nreasoning_effort = \"extreme\"\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text("[editor]\nunknown = 1\n")
            with self.assertRaises(ConfigError):
                load_config(path)

            path.write_text("[practice]\nreview_archive_ttl_days = 3651\n")
            with self.assertRaises(ConfigError):
                load_config(path)


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
