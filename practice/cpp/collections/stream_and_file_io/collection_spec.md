# Stream and File I/O

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 20 Level A exercises.
- 20 `.cpp` learner files and 20 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from line input and stream-state recovery through file modes, positioning, bounded byte transfer, stream-buffer copying, and C++20 string-stream buffer moves.

## Language Boundary

This is an up-to-C++20 collection. It targets standard stream and file-stream facilities available in C++20.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train practical stream state, unformatted input and output, file opening modes, seeking, exact bounded transfer, and ownership-aware string-stream buffer operations.

## Included Topics

- Complete-line and delimiter-based input with `std::getline`.
- Safe transitions between formatted extraction and line input.
- Reading through normal EOF, detecting non-EOF failure, and recovering after a failed record.
- Writing a specified record through a caller-provided `std::ostream&`.
- Opening C++ file streams for ordinary input, append output, truncating output, and binary input positioned at the end, with explicit open-failure reporting.
- Clearing stream state when required, seeking and rewinding input, querying opaque positions, and patching seekable output.
- Exact byte reads and writes through caller-provided spans, including transferred-count or stream-state validation.
- Copying through stream-buffer iterators, borrowing a C++20 string-stream buffer as a view, and moving string-stream buffers in or out without an avoidable string copy.

## Excluded Topics

- Typed string-stream parsing, manipulators, quoted fields, regular expressions, character conversion, and formatting already covered by the text-processing collection.
- Path manipulation, filesystem metadata, directory traversal, and filesystem mutation already covered by the filesystem collection.
- C `FILE*` ownership already covered by the ownership and RAII collection.
- `std::osyncstream` already covered by the concurrency collection.
- Console interaction, machine-specific files, temporary-file policy, memory mapping, locale-heavy parsing, and C++23 stream facilities.

## Runtime Contract

File exercises receive paths from the caller. Tests should use caller-owned temporary paths. Byte-transfer exercises state that span sizes fit `std::streamsize`. Exercises do not rely on terminal behavior or platform text translation when exact bytes matter.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/stream_and_file_io c++20
```
