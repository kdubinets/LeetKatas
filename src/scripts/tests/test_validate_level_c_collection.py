from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_level_c_collection import (  # noqa: E402
    CollectionValidationError,
    validate_collection,
)


class LevelCCollectionValidationTests(unittest.TestCase):
    def make_collection(self, root: Path) -> tuple[Path, Path, Path]:
        source = root / "problems" / "medium" / "1.md"
        source.parent.mkdir(parents=True)
        source.write_text("# Source problem\n", encoding="utf-8")

        collection = root / "collection"
        cards = collection / "cards"
        cards.mkdir(parents=True)
        (collection / "collection.json").write_text(
            json.dumps({"schema_version": 1, "id": "example.level_c.seed"}),
            encoding="utf-8",
        )
        (collection / "collection_spec.md").write_text("# Spec\n", encoding="utf-8")
        (collection / "problem_order.md").write_text("problem-1\n", encoding="utf-8")
        brief = cards / "problem-1.brief.md"
        brief.write_text("# Example Problem\n\nSolve the focused problem.\n", encoding="utf-8")
        card = cards / "problem-1.card.json"
        card.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "problem-1",
                    "source": {
                        "provider": "example-source",
                        "problem_id": "1",
                        "title": "Example Problem",
                        "difficulty": "medium",
                        "url": "https://example.test/problems/1/",
                        "local_path": "problems/medium/1.md",
                        "content_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    },
                    "teaching": {
                        "hint": "Focus on the boundary.",
                        "solution_outline": {
                            "decisive_insight": "Use the decisive structure.",
                            "approach": "Apply the approach.",
                            "state_and_invariant": "Maintain the invariant.",
                            "correctness": "The invariant proves the result.",
                            "complexity": "O(n) time and O(1) space.",
                            "pitfall": "Do not cross the boundary.",
                        },
                        "accepted_alternatives": [],
                        "tags": ["example"],
                        "prerequisites": [],
                        "common_wrong_turns": [],
                        "source_fidelity_notes": [],
                    },
                }
            ),
            encoding="utf-8",
        )
        return collection, brief, card

    def test_repository_seed_collection_is_valid(self) -> None:
        collection = (
            REPOSITORY_ROOT
            / "practice"
            / "problem_solving"
            / "collections"
            / "initial_seed"
        )

        response = validate_collection(collection)

        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["card_count"], 6)
        self.assertEqual(
            response["problem_ids"],
            ["problem-2", "problem-4", "problem-8", "problem-10", "problem-15", "problem-23"],
        )

    def test_rejects_incomplete_canonical_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection, _, _ = self.make_collection(root)
            (collection / "problem_order.md").write_text("problem-2\n", encoding="utf-8")

            with self.assertRaisesRegex(CollectionValidationError, "matching brief file"):
                validate_collection(collection, root)

    def test_rejects_private_content_in_brief(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection, brief, _ = self.make_collection(root)
            brief.write_text(
                "# Example Problem\n\nsolution_outline: secret\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(CollectionValidationError, "private teaching field"):
                validate_collection(collection, root)

    def test_rejects_stale_source_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection, _, card = self.make_collection(root)
            document = json.loads(card.read_text(encoding="utf-8"))
            document["source"]["content_sha256"] = "0" * 64
            card.write_text(json.dumps(document), encoding="utf-8")

            with self.assertRaisesRegex(CollectionValidationError, "source hash is stale"):
                validate_collection(collection, root)

    def test_rejects_unknown_versioned_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection, _, card = self.make_collection(root)
            document = json.loads(card.read_text(encoding="utf-8"))
            document["teaching"]["new_field"] = "requires a schema migration"
            card.write_text(json.dumps(document), encoding="utf-8")

            with self.assertRaisesRegex(CollectionValidationError, "unknown field"):
                validate_collection(collection, root)

    def test_rejects_incomplete_solution_outline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collection, _, card = self.make_collection(root)
            document = json.loads(card.read_text(encoding="utf-8"))
            del document["teaching"]["solution_outline"]["correctness"]
            card.write_text(json.dumps(document), encoding="utf-8")

            with self.assertRaisesRegex(CollectionValidationError, "missing required field"):
                validate_collection(collection, root)

    def test_cli_preserves_json_stdout_protocol_on_error(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPTS / "validate_level_c_collection.py")],
            input="[]",
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"error": "request must be a JSON object"})
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
