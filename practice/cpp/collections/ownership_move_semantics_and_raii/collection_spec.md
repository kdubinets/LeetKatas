# Ownership, Move Semantics, and RAII

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 36 Level A exercises.
- 36 `.cpp` learner files and 36 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from exclusive ownership through shared observation, moves, value types, and deterministic cleanup.

## Language Boundary

This is an up-to-C++20 collection. It targets idiomatic C++ facilities available through C++20 rather than a version-delta curriculum.

## Level and Purpose

These atomic exercises train explicit ownership decisions, safe ownership transfer, moved-from object handling, rule-of-zero composition, small move-aware resource types, and scope-based cleanup. A prepared learner should normally complete each task in about one minute or less.

## Included Topics

- `std::unique_ptr`, `std::shared_ptr`, and `std::weak_ptr` construction, transfer, observation, cloning, polymorphic conversion, and release patterns.
- Safe shared ownership of `this` through an existing control block.
- Move construction and assignment at use sites, valid moved-from reuse, and implicit move on return.
- Rule-of-zero storage and small handle types with focused special-member operations.
- Deterministic cleanup for memory and non-memory resources, including custom deleters and scope guards.

## Excluded Topics

- Raw owning `new`/`delete` in learner solutions except when adopting or releasing through an explicitly supplied legacy boundary.
- Concurrency primitives, which belong to the dedicated concurrency collection.
- Perfect forwarding and template mechanics, which belong to the templates and concepts collection.
- Multi-stage resource-management designs and exception-safety puzzles.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/ownership_move_semantics_and_raii c++20
```
