# C++20 Language Features

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 15 Level A exercises.
- 15 `.cpp` learner files and 15 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical order progressing from initialization and scoped-name conveniences through lambda, attribute, and preprocessing forms.

## Language Boundary

This is a C++20 language-delta collection. Each exercise targets syntax or core-language behavior added in C++20 rather than an earlier feature merely compiled as C++20.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train direct recognition and use of practical C++20 language forms.

## Included Topics

- Designated and parenthesized aggregate initialization.
- Range-for initializers, `using enum`, and conditional `explicit`.
- Pack init-captures, lambdas in unevaluated contexts, and C++20 captureless-lambda construction.
- `char8_t`, reason-bearing `[[nodiscard]]`, `[[no_unique_address]]`, branch-likelihood attributes, and `__VA_OPT__`.

## Excluded Topics

- Concepts and requires syntax, template lambda parameter lists, three-way comparison, and constant-evaluation facilities, which are owned by dedicated collections.
- Library additions, modules (which need non-atomic build support), deprecated implicit `this` capture, and implementation-dependent extended floating-point types.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/cpp20_language_features c++20
```
