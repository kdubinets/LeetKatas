# Custom Value Types and Comparisons

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 21 Level A exercises.
- 21 `.cpp` learner files and 21 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical order progressing from value equality and three-way comparison to ordered and unordered key policies.

## Language Boundary

This is an up-to-C++20 collection. It targets C++20 rewritten comparisons, comparison categories, defaulted comparison operators, transparent comparators, and standard associative-container customization.

## Level and Purpose

These atomic exercises train coherent value semantics and the ordering, hashing, and equality contracts needed to use custom types safely. A prepared learner should normally complete each task in about one minute or less.

## Included Topics

- Defaulted and custom equality, hidden-friend operators, defaulted and custom three-way comparison, and strong, weak, and partial ordering.
- Lexicographic composition, comparison-category interpretation, and strict weak ordering for named policies.
- Custom types in maps and sets, safe key replacement, defining and consuming transparent lookup policies, consistent custom hash/equality policies, and `std::hash` specialization.

## Excluded Topics

- Ordinary scalar and range comparisons, pair sorting, and record sorting already covered by core.
- Locale collation, inheritance-heavy operator designs, approximate floating-point equality, and comparison-law puzzles.

## Format and Validation

Exercise pairs follow `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/custom_value_types_and_comparisons c++20
```
