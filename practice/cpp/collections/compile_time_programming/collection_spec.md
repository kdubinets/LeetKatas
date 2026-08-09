# Compile-Time Programming

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 18 Level A exercises.
- 18 `.cpp` learner files and 18 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from constexpr declarations through constant-evaluable algorithms and storage to immediate functions, static initialization, evaluation-path selection, and C++20 constexpr object-model features.

## Language Boundary

This is an up-to-C++20 collection. It focuses on useful constant evaluation and the `constexpr`, `consteval`, and `constinit` facilities available through C++20.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train writing code that is genuinely useful during constant evaluation while keeping template metaprogramming, language-lawyer prediction, and compiler-limit experiments out of scope.

## Included Topics

- `constexpr` functions, constructors, member functions, destructors, loops, mutation, and virtual dispatch.
- Representative C++20 constant-evaluable standard algorithms and temporary use of `std::vector` and `std::string`.
- Temporary dynamic allocation whose storage is released during constant evaluation.
- Compile-time validation with `static_assert`, immediate functions, and immediate lambdas.
- Constant initialization with `constinit`, evaluation-sensitive implementation with `std::is_constant_evaluated`, and compile-time lookup-table construction.

## Excluded Topics

- Template traits, folds, concepts, and `if constexpr` type branching already owned by the templates-and-concepts collection.
- Ordinary algorithms and container operations already covered elsewhere when constant evaluation would only change the spelling of a test.
- Recursive template metaprogramming, compiler limits, undefined reads, constexpr acceptance trivia, and raw-storage lifetime puzzles.
- C++23 additions such as `if consteval`, constexpr `unique_ptr`, constexpr `bitset`, and expanded constexpr character conversion.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. The target standard library must implement C++20 constant-evaluable `std::vector` and `std::string`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/compile_time_programming c++20
```
