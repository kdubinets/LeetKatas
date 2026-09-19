# Interval Merging and Sweep Events

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

The initial set contains four exercises. Reassessment found no additional candidate with a distinct enough invariant: union length repeats active-interval merging, maximum overlap repeats room counting, and interval scheduling introduces a different greedy-selection family. The collection intentionally stays compact.

## Contract

The interval convention, input ordering, disjointness, endpoint inclusion, and equal-time event rule are supplied. Learners implement one active-interval, paired-frontier, or event-count invariant in 3–8 minutes.

## Included State Shapes

- Extend or emit one active closed interval.
- Place one incoming interval across before/overlap/after phases.
- Advance the interval whose right endpoint is exhausted.
- Process half-open meeting starts and ends with end-before-start ties.

## Exclusions

Heap frontiers, greedy interval selection, calendars, arbitrary event models, and variants differing only in endpoint type are outside this collection.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/interval_merging_and_sweep_events c++20
```

Runtime checks should compare normalized point coverage and brute-force concurrency, with nested intervals, shared endpoints, empty inputs, and equal meeting boundaries.
