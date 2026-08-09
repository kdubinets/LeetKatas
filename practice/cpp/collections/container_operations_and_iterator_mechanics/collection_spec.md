# Container Operations and Iterator Mechanics

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 23 Level A exercises.
- 23 `.cpp` learner files and 23 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from container-specific sequence operations through node transfer and unordered capacity to legacy iterator adaptors, ranges result objects, and iterator customization points.

## Language Boundary

This is an up-to-C++20 collection. It targets idiomatic container, iterator, algorithm, and ranges facilities available in C++20.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train interfaces and invalidation rules that differ materially from ordinary vector or associative-container operations, plus practical bridges between iterator-oriented and C++20 ranges code.

## Included Topics

- Adding and removing values at both ends of `std::deque`.
- List-owned stable sorting, sorted node merging, and whole-list and range node transfer with `std::list::splice`.
- C++20 removal counts from `std::list::remove_if` and `std::list::unique`.
- Predecessor-based insertion, erasure, and node transfer with `std::forward_list`.
- Retrieving all mapped values for one `std::multimap` key.
- Node transfer between compatible associative containers and the treatment of colliding keys.
- Reserving unordered-container capacity before known bulk insertion.
- Advancing non-random-access iterators; using front and positional insertion adaptors; and constructing and erasing through reverse iterators where their behavior matters.
- Consuming a C++20 ranges algorithm result whose input and output progress differ.
- Moving and swapping through iterators with customization-aware operations.

## Excluded Topics

- Ordinary vector mutation, generic algorithms, common associative lookup, iterator distance, and erase-during-iteration patterns already covered by the core collection.
- Lazy views, iterator-sentinel adaptation, subranges, borrowing, and materialization already covered by the non-owning views and ranges collection.
- Repeating ordinary map, set, queue, stack, or algorithm operations solely on a different element type.
- Custom iterator or container implementation, allocator mechanics, invalidation puzzles, undefined behavior, and C++23 range insertion or construction.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/container_operations_and_iterator_mechanics c++20
```
