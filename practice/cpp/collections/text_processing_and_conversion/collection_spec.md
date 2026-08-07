# Text Processing and Conversion

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 28 Level A exercises.
- 28 `.cpp` learner files and 28 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from character conversion through streams, regular-expression APIs, and formatting.

## Language Boundary

This is an up-to-C++20 collection. It targets idiomatic facilities available in C++20. `std::format` exercises are included because the selected C++20 toolchain provides the standard facility.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train allocation-aware numeric conversion, bounded output, conventional stream extraction and formatting, and C++20 formatted text construction beyond the core collection.

## Included Topics

- `std::from_chars` for prefix, hexadecimal, floating-point, and explicit error-category parsing.
- `std::to_chars` for decimal, hexadecimal, floating-point, and caller-supplied-buffer output.
- Stream extraction for mixed fields, textual booleans, hexadecimal input, and quoted strings.
- Stream formatting for fixed precision, padded fields, and quoted output.
- Regular-expression construction and errors, whole matching, searching, capture inspection, match and token iteration, and replacement behavior.
- C++20 `std::format`, `std::format_to`, `std::format_to_n`, and `std::vformat` for structured, aligned, bounded, appended, and runtime-selected formatting.

## Excluded Topics

- String splitting, joining, replacement, case conversion, and exact decimal integer parsing already covered by the core collection.
- String-view slicing, incremental delimiter parsing, and range-based tokenization already covered by the non-owning views and ranges collection.
- Regular-expression language instruction, locale-heavy conversion, long parsers, and C++23 formatting additions.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/text_processing_and_conversion c++20
```
