# Exercise Collections

Each exercise collection lives in its own descriptively named subdirectory. The completed [core collection](core/collection_spec.md) establishes the baseline layout; create follow-up collections alongside it.

## Required Collection Files

```text
collections/<collection_name>/
├── collection_spec.md
├── exercise_manifest.md
├── <exercise_name>.cpp
└── <exercise_name>.md
```

The collection specification must define:

- Purpose and learner level.
- Target language boundary, including whether it is up-to-version or version-delta.
- Expected exercise granularity.
- Included and excluded topic families.
- Validation standard and any toolchain requirements.
- Current status: planned, active, or frozen.

The manifest must identify each exercise's primary skill clearly enough to detect overlap.

Use [CppFollowUpTopics.md](../CppFollowUpTopics.md) to select and prioritize future collections.
