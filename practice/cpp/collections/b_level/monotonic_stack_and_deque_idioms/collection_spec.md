# Monotonic Stack and Deque Idioms

## Status

Active provisional Level B collection designed from general considerations without LeetCode corpus extraction. It is not corpus-audited, complete, or frozen.

Five initial exercises cover unresolved indices, ordered boundaries, spans, deque expiration, and rectangle boundaries. Reassessment retained two additional exercises because a bounded greedy pop budget and the two-ended prefix-deque invariant add distinct state decisions. We rejected story-only next-greater variants, separate temperature/span renamings, and contribution-sum problems whose arithmetic would dominate the monotonic invariant.

## Contract

This up-to-C++20 collection supplies the ordering, equality, expiration, and boundary rules. Learners implement one monotonic-state invariant in 3–8 minutes rather than discover the algorithm. Finish describes only observable results and constraints. Pattern is a separately folded hint followed by a blank spacer.

## Included State Shapes

- Unresolved indices awaiting a strictly greater value.
- Candidate boundary indices after removing non-smaller values.
- Previous-greater boundaries converted to spans.
- A decreasing deque with explicit expiration.
- Nondecreasing height starts finalized by shorter boundaries.
- A monotonic greedy stack with a bounded removal budget.
- An increasing prefix-sum deque with front satisfaction and back domination.

## Exclusions

Ordinary binary search, generic stack/deque API drills, duplicated next-greater stories, and problems combining several independently selected algorithms remain outside this collection.

## Verification

Validate with:

```bash
tools/validate_exercises.sh collections/b_level/monotonic_stack_and_deque_idioms c++20
```

Targeted runtime checks should compare recorded solutions with brute-force references for equality rules, duplicate values, expiration boundaries, trailing stack finalization, leftover removal budget, negative inputs, and absent results.
