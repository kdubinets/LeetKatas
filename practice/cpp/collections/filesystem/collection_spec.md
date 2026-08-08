# Filesystem

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 37 Level A exercises.
- 37 `.cpp` learner files and 37 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from lexical paths through filesystem queries and mutations to directory traversal.

## Language Boundary

This is an up-to-C++20 collection. It targets the standard `<filesystem>` library available since C++17, compiled and reviewed in the project's C++20 environment.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train portable path manipulation, explicit selection of throwing or non-throwing operations, filesystem metadata queries, common mutations, and iterator-based directory traversal.

## Included Topics

- Path joining and direct concatenation, decomposition, filename and extension replacement, lexical normalization and relativity, component iteration, and portable generic-string conversion.
- Existence and file-type queries, symlink-aware status and target reading, absolute, canonical, weakly canonical, and filesystem-relative paths, plus equivalence checks.
- Non-throwing directory creation, file and tree copying, resizing, renaming, removal, permission updates, modification-time queries and updates, and space queries.
- Direct and recursive directory iteration, regular-file filtering, subtree pruning, and explicit iterator error handling.

## Excluded Topics

- Non-throwing file-size propagation already covered by the variants and error-modelling collection.
- C `FILE*` ownership already covered by the ownership and RAII collection.
- Platform-specific path encodings, native separator assumptions, temporary-file policy, file contents, stream I/O, memory mapping, and operating-system watch APIs.
- Hard-link, symlink, and permission-policy scenarios that require elevated privileges or platform-specific runtime fixtures.

## Runtime Contract

Exercises that touch the filesystem receive their paths from the caller. Throwing overload exercises allow `std::filesystem::filesystem_error` to propagate. Non-throwing overload exercises expose a caller-owned `std::error_code`; callers must inspect it before using a sentinel or partial result.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/filesystem c++20
```
