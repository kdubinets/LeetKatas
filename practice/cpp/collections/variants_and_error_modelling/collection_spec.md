# Variants and Error Modelling

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 21 Level A exercises.
- 21 `.cpp` learner files and 21 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical order progressing from variant state handling to explicit error values and exception boundaries.

## Language Boundary

This is an up-to-C++20 collection. It uses C++20 `std::variant`, `std::optional`, exceptions, and `std::error_code`; it does not use C++23 monadic member functions or `std::expected`.

## Level and Purpose

These atomic exercises train safe inspection, extraction, mutation, and visitation of sum types, plus concise translation between absence, explicit errors, exceptions, and error codes. A prepared learner should normally complete each task in about one minute or less.

## Included Topics

- Variant construction, alternative tests, pointer-style access, emplacement, single- and multi-variant visitation, overloaded visitors, and `std::monostate`.
- Manual C++20 optional composition where it represents a distinct operation rather than basic fallback or lookup.
- Converting absence into an explicit error, transforming and chaining success-or-error results, deterministic multi-result propagation, exception translation, rethrowing with context, and `std::error_code` boundaries.

## Excluded Topics

- Basic optional fallback, container lookup, and numeric parsing already covered by core.
- C++23 `std::expected` and monadic `std::optional` operations.
- Exception-safety proofs, custom exception hierarchies, and multi-stage parsers.

## Format and Validation

Exercise pairs follow `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/variants_and_error_modelling c++20
```
