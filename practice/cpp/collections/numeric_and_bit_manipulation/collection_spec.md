# Numeric and Bit Manipulation

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 26 Level A exercises.
- 26 `.cpp` learner files and 26 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from bit utilities and masks to safe numeric operations, reductions, and randomization.

## Language Boundary

This is an up-to-C++20 collection. It targets idiomatic facilities available in C++20 and uses unsigned types where bit operations require defined shift behavior.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They deepen practical use of C++20 bit utilities, masks and bitsets, safe mixed-type numeric operations, reductions, rounding, interpolation, random engines, and random algorithms beyond the core collection.

## Included Topics

- `<bit>` power-of-two queries, bit width, leading and trailing zero counts, bit floors and ceilings, rotation, and representation-safe bit casting.
- Safe low-bit masks, flag tests and updates, field extraction and replacement, and `std::bitset` mutation.
- Representability checks and safe signed/unsigned comparison.
- Interpolation and explicit rounding behavior.
- Parallelization-ready reduction and transformed reduction forms.
- Deterministic engine construction, uniform distributions, shuffling, and sampling.

## Excluded Topics

- Popcount, GCD, midpoint, clamping, ordinary accumulation, prefix scans, adjacent differences, and arithmetic progression generation already covered by the core collection.
- C++23 utilities such as `std::byteswap` and newer checked or saturating arithmetic proposals.
- Cryptographic randomness, statistical testing, undefined signed shifts, and manual bit-hack trivia.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/numeric_and_bit_manipulation c++20
```
