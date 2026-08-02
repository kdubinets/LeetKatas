# Exercise Collections

Each exercise collection lives in its own descriptively named subdirectory. The completed [core collection](core/collection_spec.md) establishes the baseline layout; create follow-up collections alongside it.

## Required Collection Files

```text
collections/<collection_name>/
├── environment.json             # optional machine-readable target environment
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

An optional `environment.json` supplies the target language version, available
libraries, and restrictions to the evaluation harness and reviewer. It describes
what is available, not what an exercise must use; technique requirements belong
in the exercise metadata. For example:

```json
{
  "language": {
    "name": "C++",
    "version": "C++20"
  },
  "libraries": [
    {
      "name": "C++ standard library",
      "version": "C++20"
    }
  ],
  "restrictions": [
    "No third-party libraries"
  ]
}
```

`language.name` and `language.version` are required non-empty strings.
`implementation` may optionally identify a runtime or compiler, while
`libraries` and `restrictions` are optional arrays. Library entries require a
name and may include a version.

An optional `exercise_order.md` defines a canonical introduction order. It must
contain every exercise basename exactly once, one unadorned basename per line.

Use [CppFollowUpTopics.md](../CppFollowUpTopics.md) to select and prioritize future collections.
