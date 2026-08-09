# Templates and Concepts

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 36 Level A exercises.
- 36 `.cpp` learner files and 36 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical order progressing from template fundamentals through packs and traits to C++20 constraints.

## Language Boundary

This is an up-to-C++20 collection. It teaches practical template and constraint forms available in C++20.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. Supporting types make each required relationship observable without requiring template metaprogram design or algorithm discovery.

## Included Topics

- Function, member-function, class, alias, variable, and deduction-guide syntax.
- Default template arguments and dependent type and member-template names.
- Explicit and partial specialization.
- Parameter packs, pack expansion, and fold expressions.
- Common type transformations, compile-time branching, and detection.
- Named concepts, requires-expressions, compound and nested requirements, abbreviated templates, and constrained overloads.

## Excluded Topics

- Generic and explicit-template lambdas, callable forwarding, comparison policies, and variant visitation already owned by other collections.
- Template-template parameters, recursive metaprogramming, expression SFINAE puzzles, and other forms too exotic for Level A fluency.
- Compile-time evaluation facilities such as `consteval` and `constinit`, which belong to the compile-time programming collection.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/templates_and_concepts c++20
```
