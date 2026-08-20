from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parents[1]
COLLECTION = (
    REPOSITORY_ROOT
    / "practice"
    / "problem_solving"
    / "collections"
    / "algorithmic_problem_solving"
)
FAKE = REPOSITORY_ROOT / "src" / "nvim-driver" / "tests" / "fake_level_c_reviewer.py"
sys.path.insert(0, str(SCRIPTS))

import level_c_codex  # noqa: E402
from level_c_codex import build_prompt  # noqa: E402
from level_c_conversation import clarify, discuss  # noqa: E402
from level_c_conversation_protocol import (  # noqa: E402
    ConversationError,
    conversation_request,
    validate_clarification_response,
    validate_discussion_response,
    validate_history,
)
from practice_scheduler import SchedulerError  # noqa: E402
from problem_solving_card import card_action  # noqa: E402
from problem_solving_store import ProblemSolvingStore  # noqa: E402


class LevelCConversationTests(unittest.TestCase):
    def request(self, database: Path, **values) -> dict:
        return {
            "collection_directory": str(COLLECTION),
            "database_path": str(database),
            "problem_id": "problem-2",
            "reviewer": {
                "command": [sys.executable, str(FAKE)],
                "name": "Fake Level C",
                "model": "fake-model",
                "reasoning_effort": "low",
            },
            **values,
        }

    def test_strict_response_schemas_and_alternating_history(self) -> None:
        self.assertEqual(validate_history([]), [])
        with self.assertRaisesRegex(ConversationError, "alternate"):
            validate_history([{"role": "assistant", "content": "no"}])
        with self.assertRaisesRegex(ConversationError, "only"):
            validate_clarification_response(
                {"status": "answered", "answer": "yes", "disclosure": "clarification", "extra": 1}
            )
        with self.assertRaisesRegex(ConversationError, "status"):
            validate_discussion_response(
                {"status": "redirected", "answer": "no", "references": [], "follow_up_suggestions": []}
            )

    def test_clarification_payload_never_contains_private_teaching_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            request = self.request(Path(temporary) / "practice.sqlite3", question="What is first?")
            captured = {}

            def fake_call(mode, payload, command):
                captured.update(payload)
                return {
                    "status": "available",
                    "attempts": 1,
                    "response": {
                        "status": "answered",
                        "answer": "The head is the least-significant digit.",
                        "disclosure": "clarification",
                    },
                    "failure": None,
                }

            with patch("level_c_conversation.conversation_request", side_effect=fake_call):
                response = clarify(request)

            serialized = json.dumps(captured)
            self.assertEqual(response["status"], "answered")
            self.assertNotIn("solution_outline", serialized)
            self.assertNotIn("decisive_insight", serialized)
            self.assertNotIn("optional_hint\"", serialized)

    def test_clarification_redirect_and_local_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            response = clarify(
                self.request(database, question="Which algorithm and approach should I use?")
            )

            self.assertEqual(response["status"], "redirected")
            self.assertEqual(response["disclosure"], "none")
            artifact = ProblemSolvingStore(database).artifact(
                "leetkatas.problem_solving.initial_seed", "problem-2"
            )
            self.assertTrue(artifact["clarification_used"])
            self.assertEqual(len(artifact["conversation_history"]), 2)

    def test_retention_disabled_keeps_history_out_of_sqlite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            response = clarify(
                self.request(
                    database,
                    question="Which digit is at the head?",
                    retain_conversation_history=False,
                )
            )

            self.assertEqual(len(response["conversation_history"]), 2)
            artifact = ProblemSolvingStore(database).artifact(
                "leetkatas.problem_solving.initial_seed", "problem-2"
            )
            self.assertEqual(artifact["conversation_history"], [])

    def test_new_turn_keeps_only_the_latest_sixteen_messages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            store = ProblemSolvingStore(database)
            history = []
            for index in range(8):
                history.extend(
                    [
                        {"role": "user", "content": f"question {index}"},
                        {"role": "assistant", "content": f"answer {index}"},
                    ]
                )
            store.update_artifact(
                "leetkatas.problem_solving.initial_seed",
                "problem-2",
                conversation_history=history,
            )

            response = clarify(
                self.request(database, question="Which digit is at the head?")
            )

            self.assertEqual(len(response["conversation_history"]), 16)
            self.assertEqual(response["conversation_history"][0]["content"], "question 1")
            self.assertEqual(response["conversation_history"][-2]["content"],
                             "Which digit is at the head?")

    def test_discussion_is_gated_and_receives_revealed_material(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            request = self.request(database, question="Why is the invariant sufficient?")
            with self.assertRaisesRegex(SchedulerError, "only after"):
                discuss(request)
            card_action({**request, "action": "reveal"})

            captured = {}

            def fake_call(mode, payload, command):
                captured.update(payload)
                return {
                    "status": "available",
                    "attempts": 1,
                    "response": {
                        "status": "answered",
                        "answer": "It preserves every processed digit.",
                        "references": ["outline:correctness"],
                        "follow_up_suggestions": [],
                    },
                    "failure": None,
                }

            with patch("level_c_conversation.conversation_request", side_effect=fake_call):
                response = discuss(request)

            self.assertIn("solution_outline", captured["problem"])
            self.assertEqual(response["references"], ["outline:correctness"])

    def test_adapter_failure_is_categorical_and_does_not_persist_question(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "practice.sqlite3"
            response = clarify(self.request(database, question="UNAVAILABLE"))

            self.assertEqual(response["status"], "unavailable")
            self.assertEqual(response["failure"], "reviewer_exited_unsuccessfully")
            self.assertNotIn("private adapter failure", json.dumps(response))
            artifact = ProblemSolvingStore(database).artifact(
                "leetkatas.problem_solving.initial_seed", "problem-2"
            )
            self.assertEqual(artifact["conversation_history"], [])

    def test_runner_retries_malformed_adapter_output(self) -> None:
        result = conversation_request(
            "clarification",
            {"question": "q"},
            [sys.executable, "-c", "print('not json')"],
        )
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(result["failure"], "malformed_reviewer_json")

    def test_cli_errors_remain_json_only(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "level_c_clarify.py")],
            input="[]",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"error": "request must be a JSON object"})
        self.assertEqual(result.stderr, "")

    def test_codex_modes_use_distinct_prompts(self) -> None:
        clarification = build_prompt("clarification", {"question": "q"})
        discussion = build_prompt("discussion", {"question": "q"})
        self.assertIn("Do not reveal or imply an algorithm", clarification)
        self.assertNotIn("canonical solution outline has been revealed", clarification)
        self.assertIn("canonical solution outline has been revealed", discussion)

    def test_level_c_codex_always_ignores_user_config(self) -> None:
        commands: list[list[str]] = []

        def run(command, **unused):
            commands.append(command)
            output = Path(command[command.index("--output-last-message") + 1])
            output.write_text("{}", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        stdout = io.StringIO()
        with (
            patch.object(sys, "argv", ["level_c_codex.py", "--mode", "clarification"]),
            patch.object(sys, "stdin", io.StringIO("{}")),
            patch.object(sys, "stdout", stdout),
            patch("level_c_codex.subprocess.run", side_effect=run),
        ):
            returncode = level_c_codex.main()

        self.assertEqual(returncode, 0)
        self.assertIn("--ignore-user-config", commands[0])
        self.assertEqual(json.loads(stdout.getvalue()), {})


if __name__ == "__main__":
    unittest.main()
