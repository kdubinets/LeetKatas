# C++ Exercise Collections

This directory contains focused C++ practice collections and the documentation used to grow and validate them.

## Layout

```text
cpp/
├── AGENTS.md
├── README.md
├── CppFollowUpTopics.md
├── CppProblemsGenerationPrompt.md
├── collections/
│   ├── README.md
│   └── core/
│       ├── collection.json
│       ├── collection_spec.md
│       ├── environment.json
│       ├── exercise_manifest.md
│       ├── exercise_order.md
│       └── 108 exercise pairs
└── tools/
    └── validate_exercises.sh
```

## Current Collection

The [core collection](collections/core/collection_spec.md) contains 108 Level A implementation-fluency exercises targeting idiomatic C++ up to and including C++20. It is considered complete and should normally remain frozen.

Its [exercise order](collections/core/exercise_order.md) records the canonical
1-to-108 progression as one exercise basename per line. The
[exercise manifest](collections/core/exercise_manifest.md) records generation
batch, primary implementation skill, and supporting topics.

## Planning Documents

- [Follow-up topics](CppFollowUpTopics.md) lists proposed up-to-C++20 collections and a separate C++23-delta curriculum.
- The [base generation prompt](CppProblemsGenerationPrompt.md) defines the exercise-pair format and general quality requirements.

## Validation

Validate the core collection from this directory with:

```bash
tools/validate_exercises.sh collections/core c++20
```

The validator compiles temporary completed forms through a pipe; it does not modify learner files or leave generated solutions in the repository.

## Adding a Collection

1. Create `collections/<descriptive_name>/`.
2. Write `collection_spec.md` before generating exercises.
3. Add `collection.json` with a stable, globally unique ID when progress should be portable or syncable.
4. Add `environment.json` when the evaluation harness should receive explicit target-language, library, or tool restrictions.
5. Create `exercise_manifest.md` and treat it as the collection inventory.
6. Add `exercise_order.md` when the collection has a canonical introduction order.
7. Generate and validate exercises in reviewable batches.
8. Reassess gaps after each batch and freeze the collection when only weak variants remain.
