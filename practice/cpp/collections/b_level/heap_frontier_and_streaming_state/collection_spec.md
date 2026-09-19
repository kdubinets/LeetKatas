# Heap Frontier and Streaming State

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

Four initial exercises cover a multi-sequence frontier, a bounded best-candidate heap, stale weighted-distance entries, and balanced lower/upper halves. Reassessment found no addition worth the overlap: heap-based meeting rooms repeats the interval collection, kth-largest variants repeat bounded retention, and repeated two-item reductions are too close to Level A heap mechanics.

## Contract

The heap role, entry meaning, ordering, stale-entry rule, and balance invariant are supplied. Learners implement one frontier invariant in 3–8 minutes rather than discover the algorithm or configure an isolated heap.

## Included State Shapes

- One current entry per nonexhausted sorted input.
- A reversed bounded heap retaining the globally smallest values seen.
- Tentative weighted distances with stale heap entries skipped.
- Two heaps partitioning a stream into balanced lower and upper halves.

## Exclusions

Heap API drills, interval concurrency, A* search, custom data structures, and story variants of top-k selection are excluded.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/heap_frontier_and_streaming_state c++20
```

Runtime checks should compare randomized inputs with full sorting, simple shortest-path references, and sorted stream prefixes.
