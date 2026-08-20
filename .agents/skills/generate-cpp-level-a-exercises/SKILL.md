---
name: generate-cpp-level-a-exercises
description: Generate a new LeetKatas Level A C++ implementation-fluency exercise collection, or extend an existing non-core one. Use when asked to create, grow, or batch-generate atomic C++ API-fluency exercises (as opposed to Level B idioms or full algorithm-discovery problems), such as a new library-fluency collection like chrono or filesystem. Do not use on `collections/core`, which is frozen.
---

# Generate C++ Level A Exercises

Produce atomic C++ implementation-fluency exercise pairs using the canonical
generation format, then wire the result into this repository's collection
rules so the batch is actually usable and de-duplicated against what already
exists.

## Read first

1. `practice/cpp/AGENTS.md`
2. `practice/cpp/README.md`
3. `practice/cpp/CppProblemsGenerationPrompt.md` — the canonical exercise
   format: file pairing, the `// Finish:` marker convention, metadata
   sections, granularity, and correctness requirements. Follow it exactly for
   every exercise you generate.
4. The target collection's `collection_spec.md` and `exercise_manifest.md` if
   the collection already exists, or every existing collection's
   `exercise_manifest.md` if you are creating a new one.

`collections/core/` is frozen. Do not add, remove, or edit exercises there
unless the user explicitly asks for core changes.

## Avoid duplicates

Before generating anything, read every existing `exercise_manifest.md` under
`practice/cpp/collections/*/`. Each entry's description exists specifically to
support this check. Reject a candidate that tests essentially the same
operation as an existing exercise in any collection, not only the target one.

## Collection workflow

1. If the target collection does not exist yet, create
   `practice/cpp/collections/<descriptive_name>/` with `collection_spec.md`,
   `environment.json`, and `collection.json` (stable ID, schema version)
   before generating exercises. State the collection's target standard and
   purpose (interview mechanics, library fluency, or mixed) in
   `collection_spec.md`.
2. Generate exercise pairs following `CppProblemsGenerationPrompt.md`.
3. Update `exercise_manifest.md` — and `exercise_order.md` where the
   collection has one — in the same change as any exercise addition, removal,
   rename, or primary-skill change. This is required by `practice/cpp/AGENTS.md`
   and is not optional or deferrable to a later pass.
4. Validate the collection:

   ```bash
   practice/cpp/tools/validate_exercises.sh practice/cpp/collections/<name> c++20
   ```

   Run this from the repository root, or `tools/validate_exercises.sh
   collections/<name> c++20` from `practice/cpp/`. Fix every failure before
   handoff; the validator checks pairing, metadata structure, `// Finish:`
   marker counts, manifest coverage, and compilation after substituting every
   recorded solution.
5. Reassess the manifest after each batch for near-duplicates or weak
   variants. Stop rather than pad the collection to hit a requested count —
   `CppProblemsGenerationPrompt.md`'s counts are approximate targets, not
   quotas.

## Verification

Before handoff:

1. Confirm `exercise_manifest.md` (and `exercise_order.md` if present) lists
   every exercise pair actually present in the collection directory, and only
   those.
2. Run the validator and confirm it passes.
3. Run `git diff --check`.
