from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

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


class SelectExerciseTests(unittest.TestCase):
    def create_pair(self, directory: Path, name: str) -> None:
        (directory / f"{name}.cpp").write_text("int solve() { return 1; }\n")
        (directory / f"{name}.md").write_text(f"# Name\n\n{name}\n")

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
            self.assertEqual(response["proposed_rating"], "good")
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
            self.assertEqual(response["proposed_rating"], "fail")
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
