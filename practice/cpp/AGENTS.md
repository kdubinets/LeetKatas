# C++ Exercise Collections

## Scope

This directory is dedicated to C++ exercise collections. Keep exercise files inside a named collection directory; do not add exercise pairs directly to this directory.

Start work from this directory or a descendant so this guidance is loaded.

## Read First

- `README.md` describes the directory layout and current collection status.
- `CppProblemsGenerationPrompt.md` is the canonical base format for implementation-fluency exercises.
- `CppFollowUpTopics.md` is the roadmap for future collections.
- `LevelBInterviewIdiomsPlan.md` defines the separate Level B interview-idiom curriculum and workflow.
- Before changing a collection, read its `collection_spec.md` and `exercise_manifest.md`.

## Collection Rules

- Each collection owns its target standard, scope, granularity, and status in `collection_spec.md`.
- An unqualified C++20 collection means idiomatic C++ up to and including C++20.
- A C++23 delta collection must exercise facilities introduced in C++23 and must not repeat earlier-standard fundamentals merely compiled as C++23.
- Keep each exercise atomic and normally completable in one minute or less unless the collection specification explicitly defines another level.
- Prefer quality over requested quantity. If only duplicate, trivial, or exotic candidates remain, report that limit instead of padding the collection.
- Use descriptive lowercase snake_case basenames and keep every exercise's `.cpp` and `.md` files together in its collection directory.
- Update the collection manifest in the same change as any exercise addition, removal, rename, or primary-skill change.
- When a collection has `exercise_order.md`, update it in the same change as any exercise addition, removal, or rename.
- Review the complete manifest before proposing or generating exercises so primary objectives do not overlap.

## Existing Core Collection

- `collections/core/` contains the completed 108-exercise implementation-fluency collection.
- Treat `collections/core/` as frozen unless the user explicitly requests additions, corrections, or restructuring.
- Preserve existing exercise names and content when working on unrelated collections.
- Before proposing core additions from the solved interview-problem corpus, use the `audit-cpp-interview-fluency` skill to gather reproducible evidence. The audit itself must not change exercises.

## Future Collections

- Use the `generate-cpp-level-a-exercises` skill to create or grow a new Level A collection.
- Create Level A collections under `collections/<descriptive_name>/` and Level B interview-idiom collections under `collections/b_level/<descriptive_name>/`.
- Each new collection must begin with `collection_spec.md` and `exercise_manifest.md`.
- Record whether the collection is up-to-version or version-delta before generating exercises.
- Use a nested `AGENTS.md` only when a collection needs durable rules that genuinely differ from this file; keep ordinary collection details in `collection_spec.md`.

## Level B Interview Idioms

- Keep Level B collections separate from the frozen Level A core. They teach implementation of a named, supplied interview idiom rather than atomic library operations or algorithm discovery.
- Before planning, generating, reviewing, or extending a Level B collection, use the `develop-cpp-level-b-idioms` skill and read `LevelBInterviewIdiomsPlan.md`.
- Do not use the Level A corpus audit to decide Level B coverage. Add a dedicated Level B audit only after the initial Level B core is present.

## Validation

After changing exercise pairs or a manifest, run:

```bash
tools/validate_exercises.sh <collection-directory> <language-standard>
```

For the core collection:

```bash
tools/validate_exercises.sh collections/core c++20
```

The validator checks pairing, metadata structure, Finish-marker counts, manifest coverage, and compilation after substituting every recorded solution.

Add targeted runtime checks when an exercise has meaningful edge cases that compilation alone cannot verify.

## Change Safety

- Do not move or reorganize an existing collection unless explicitly requested.
- Do not overwrite learner files with completed solutions.
- Do not treat the generated, substituted source used for validation as a repository artifact.
- Keep meta documentation and validation tools outside collection directories unless they are collection-specific.
