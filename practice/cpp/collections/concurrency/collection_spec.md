# Concurrency

## Status

Complete and frozen unless corrections or further changes are explicitly requested.

## Inventory

- 37 Level A exercises.
- 37 `.cpp` learner files and 37 matching `.md` metadata files.
- One manifest exposing every primary implementation objective.
- One canonical exercise order progressing from thread lifetime and cancellation through locks, condition waits, atomics, C++20 coordination primitives, asynchronous results, shared-state utilities, and synchronized output.

## Language Boundary

This is an up-to-C++20 collection. It uses C++20 threads, stop tokens, mutexes, condition variables, atomic operations, latches, barriers, semaphores, futures, and atomic smart pointers.

## Level and Purpose

These are atomic implementation-fluency exercises intended to take a prepared learner about one minute or less. They train deterministic ownership and synchronization patterns without asking the learner to discover a concurrent algorithm or reproduce a race.

## Included Topics

- `std::thread`, `std::jthread`, argument handoff, joining, stop tokens, stop sources, and stop callbacks.
- `std::lock_guard`, `std::unique_lock`, early release, `std::scoped_lock`, shared locking, predicate waits, notification, and stop-aware waits.
- Atomic read-modify-write operations, relaxed statistics, compare-and-exchange, `std::atomic_ref`, release/acquire publication, atomic waiting and notification, and two-sided atomic `shared_ptr` handoff.
- C++20 latches, barriers, and semaphores.
- Promises, futures, exception propagation, explicit `std::async` policy, `std::packaged_task`, and one-time initialization.
- Non-interleaved stream emission with `std::osyncstream`.

## Excluded Topics

- Sleeps, wall-clock assumptions, probabilistic scheduling, deliberate data races, lock-free data-structure design, and exercises whose correctness depends on reproducing undefined behavior.
- Advanced memory-order proofs, relaxed-order algorithms, fences, and compare-and-exchange loops that would exceed Level A scope.
- Parallel execution policies, native thread handles, platform APIs, and thread pools not supplied by C++20.
- Atomic `weak_ptr`, because it adds API symmetry without a distinct Level A ownership handoff beyond the atomic `shared_ptr` exercise pair.

## Format and Validation

Exercise pairs follow the canonical requirements in `../../CppProblemsGenerationPrompt.md`. Validate from `practice/cpp/` with:

```bash
tools/validate_exercises.sh collections/concurrency c++20
```
