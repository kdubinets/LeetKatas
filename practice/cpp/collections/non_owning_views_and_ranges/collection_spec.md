# Non-Owning Views and Ranges

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 30 Level A exercises.
- 30 `.cpp` learner files and 30 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from spans and string views to composed and lifetime-aware range views.

## Language Boundary

This is an up-to-C++20 collection. It targets idiomatic facilities available in C++20 and does not use C++23 range materialization, folds, algorithms, or views.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They deepen non-owning access, lazy range composition, iterator/sentinel handling, and safe materialization beyond the core collection.

## Included Topics

- Dynamic- and fixed-extent `std::span`, subviews, byte views, and views into owning containers.
- `std::string_view` slicing and delimiter-, width-, and predicate-based incremental parsing without allocation.
- C++20 range adaptors including `drop`, `take`, `take_while`, `drop_while`, `filter`, `transform`, `elements`, `join`, `split`, `iota`, `counted`, `common`, and `all`.
- Iterator/sentinel subranges, borrowed iterators, returned lazy views, owning views, and lifetime-aware results.
- Explicit materialization through iterator construction or range copying where C++20 has no `std::ranges::to`.

## Excluded Topics

- Algorithms already exercised substantially by the core collection when a new task would only change syntax.
- C++23 range facilities.
- Custom view or adaptor implementation.
- Dangling-view puzzles, undefined behavior, and long parsing tasks.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/non_owning_views_and_ranges c++20
```
