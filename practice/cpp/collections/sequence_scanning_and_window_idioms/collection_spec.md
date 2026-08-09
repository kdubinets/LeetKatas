# Sequence Scanning and Window Idioms

## Status

Initial Level B core proposal. It is usable in the practice driver, but it is not complete or frozen: a dedicated Level B corpus audit must test its coverage against solved C++ interview problems before additions are proposed.

## Inventory

- 19 Level B exercises.
- 19 `.cpp` learner files and 19 matching `.md` metadata files.
- One manifest exposing the distinct implementation invariant trained by each exercise.
- One canonical order that introduces bounded scans before prefix state, range differences, and manual binary-search loop invariants.

## Language Boundary

This is an up-to-C++20 collection using only the C++20 standard library. The machine-readable `environment.json` supplies that boundary to the practice evaluator and reviewer. Inputs keep all specified arithmetic and result counts representable in their declared types.

## Level and Purpose

These are Level B exercises: the learner is given the applicable interview idiom and its invariant, then implements the associated state transitions and loop control. They do not ask the learner to discover an algorithm or combine independently chosen patterns.

An exercise should normally require 3–8 minutes. Its source contains one `// Pattern:` comment, which names the idiom and invariant without prescribing APIs or code, followed by exactly one `// Finish:` section. This explicit pattern comment is the deliberate Level B exception to the base prompt's usual comment-minimization rule; the validator permits at most one such comment.

## Included Topics

- Fixed-size rolling windows over sums and frequency state.
- Shrink-to-valid windows whose left edge restores a supplied invariant.
- Converging, opposing, backward-merge, and read/write sequence pointers.
- Prefix sums, prefix-frequency maps, and first-occurrence prefix state.
- Difference arrays for many closed range updates.
- Half-open manual binary-search loops for exact search and boundary searches.

## Excluded Topics

- Atomic standard-library operations already trained in Level A, including calling a binary-search algorithm or building a prefix-sum array without its query invariant.
- Algorithm selection, dynamic programming, monotonic stacks, trees, graphs, linked lists, heaps, and disjoint sets.
- Multi-pattern whole problems, production data modeling, I/O, and custom data-structure implementation.

## Format and Validation

Exercise pairs follow `../../CppProblemsGenerationPrompt.md` except for the documented single `// Pattern:` comment. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/sequence_scanning_and_window_idioms c++20
```
