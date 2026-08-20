---
name: develop-cpp-level-b-idioms
description: Design, create, review, or extend LeetKatas C++ Level B interview-implementation-idiom collections. Use when asked to plan or generate reusable C++ interview idiom exercises such as windows, pointers, stacks, searches, traversals, or stateful scans; keep Level B distinct from Level A atomic fluency and full algorithm-discovery problems.
---

# Develop C++ Level B Idioms

Build the bridge between Level A C++ API fluency and unaided interview-problem practice. Level B teaches implementation of a named, already-selected idiom—not discovery of its algorithm.

## Read first

Read these files before planning or changing a Level B collection:

1. `practice/cpp/AGENTS.md`
2. `practice/cpp/README.md`
3. `practice/cpp/LevelBInterviewIdiomsPlan.md`
4. `practice/cpp/CppProblemsGenerationPrompt.md`
5. The target collection's `collection_spec.md` and `exercise_manifest.md`, if it exists.

Treat `collections/core` as Level A and frozen. Do not use the Level A audit skill to justify Level B changes.

## Exercise contract

Each Level B exercise must have one recognizable idiom and one primary implementation invariant. State the pattern and invariant in the learner source, then leave its concrete implementation unfinished. For example:

```cpp
// Pattern: sliding window. Keep the current window valid by shrinking its left edge.
// Finish: return the greatest valid window length
```

The pattern may be named; do not reveal the exact API calls, data structure operations, or final code. Keep supporting code minimal, preserve exactly one `// Finish:` section, and keep the metadata's three required sections. The description must state the pattern, invariant, inputs, constraints, and intended implementation skill.

Target 3–8 minutes of learner work. Reject a candidate when it requires selecting the algorithm, combining independently selected patterns, inventing a data model, or merely renaming an existing exercise.

## Collection workflow

1. Choose one state-model family. Do not build a mixed collection merely because all items are interview-related.
2. Write the collection specification, manifest, canonical order, environment, and stable collection ID before exercise generation.
3. Review every existing Level B manifest and the Level A core manifest for overlap.
4. Generate a small reviewable batch. Give each exercise a distinct primary implementation decision.
5. Validate with `practice/cpp/tools/validate_exercises.sh <collection> c++20` and add targeted runtime checks only when their value is clear.
6. Reassess the manifest after each batch. Stop rather than pad with weak variants.
7. Do not declare the initial Level B core complete until a dedicated Level B corpus audit has checked it against solved interview solutions.

Use your strongest available reasoning setting for collection design, generation, and difficult boundary or final-review decisions.

## Scope decisions

Use these classifications when evaluating a proposed exercise:

| Classification | Action |
|---|---|
| Atomic library operation | Keep in Level A or an existing language-focused collection. |
| Named, reusable implementation idiom | Candidate for Level B. |
| Algorithm-selection or multi-pattern problem | Keep for normal problem practice. |
| Specialised professional-library task | Keep in a follow-up C++ collection, not Level B. |

One canonical exercise per idiom is the default. Add a second only when it trains a different state shape, invariant, or implementation decision; spaced repetition supplies recall practice without artificial near-duplicates.

## Corpus evidence

After the first Level B collection is present, create and use a dedicated Level B audit workflow. It must keep a separate hash-aware review ledger and classify a solution's patterns as trained, partial, candidate, duplicate variation, or out of scope. Prefer new sampled solutions over re-reviewing unchanged ones. Do not alter collections during an audit unless explicitly asked.

