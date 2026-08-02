# Core Implementation-Fluency Collection

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 108 exercises.
- 108 `.cpp` learner files.
- 108 matching `.md` metadata and solution files.
- One [exercise manifest](exercise_manifest.md) organized into four generation batches.
- One [exercise order](exercise_order.md) containing the canonical progression.

## Language Boundary

The collection targets idiomatic C++ up to and including C++20. Exercises may teach facilities introduced by earlier standards when those facilities remain appropriate C++20 practice.

The machine-readable `environment.json` supplies this C++20 target and standard-library boundary to the practice evaluator and reviewer.

## Level and Purpose

These are Level A implementation-fluency exercises. They train fast, idiomatic translation of an already-understood operation into C++ rather than algorithm discovery.

Each learner task should normally take one minute or less and must have one atomic primary objective.

## Format

The canonical requirements are defined by the [base generation prompt](../../CppProblemsGenerationPrompt.md). In particular:

- Every exercise has one lowercase snake_case basename shared by a `.cpp` and `.md` file.
- Every learner file has exactly one `// Finish:` practice section.
- Metadata contains `# Name`, `# Description`, and `# Solution` sections.
- The solution block contains exactly the replacement for the Finish-marker line.

## Validation

From the parent `cpp/` directory, run:

```bash
tools/validate_exercises.sh collections/core c++20
```
