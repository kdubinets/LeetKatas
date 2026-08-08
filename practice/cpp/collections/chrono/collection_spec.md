# Chrono

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 36 Level A exercises.
- 36 `.cpp` learner files and 36 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from durations through time points and deadlines to C++20 civil-calendar types.

## Language Boundary

This is an up-to-C++20 collection. It uses C++20 duration, clock, time-point, calendar, weekday, and time-of-day facilities. Calendar exercises assume standard-library support for the C++20 calendaring portion of `<chrono>`.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train type-safe unit conversion, time-point arithmetic, deadline calculations, and direct use of civil-calendar vocabulary without depending on wall-clock input or nondeterministic timing.

## Included Topics

- Mixed-unit duration conversion, arithmetic, comparison, absolute values, remainders, literals, and explicit floor, ceiling, and nearest rounding.
- Time-point offsets and differences, deadline checks, nonnegative remaining time, timeout-unit rounding, precision conversion, date-and-time composition, and `time_t` boundaries.
- C++20 `year_month_day`, validity checks, `sys_days`, day and month differences and shifts, month-end dates, weekdays, indexed-weekday validation, leap years, and `hh_mm_ss` decomposition and field access.

## Excluded Topics

- Scalar numeric rounding and interpolation already covered by the numeric collection.
- Sleeping, benchmarking, live calls to `now()`, and tests whose answers depend on scheduler or wall-clock timing.
- Locale-sensitive chrono parsing and formatting because portable C++20 library availability remains uneven.
- Time-zone database and `zoned_time` exercises because the required runtime database and complete C++20 implementation are not reliably available across the target toolchains.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/chrono c++20
```
