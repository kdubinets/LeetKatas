# Backtracking and Reversible State

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

Four initial exercises cover path restoration, used-marker restoration, reusable-choice pruning, and temporary grid mutation. Reassessment retained same-depth duplicate suppression and coordinated occupancy sets because they add distinct reversible-state decisions.

## Contract

The choice order, stopping condition, pruning rule, and state meaning are supplied. Learners implement one choose/recurse/undo invariant in 3–8 minutes rather than discover a search formulation. Output order is specified when observable.

## Included State Shapes

- Append and remove one path choice around recursion.
- Mark and unmark a distinct input position.
- Reuse a sorted candidate while reducing a remaining target.
- Temporarily mark a grid cell and restore it on every return path.
- Skip equal values only when they compete at the same search depth.
- Apply and undo one queen across three coupled occupancy tables.

## Exclusions

Tree traversal over an existing structure, graph visitation, unconstrained exponential puzzles, solver frameworks, and variants changing only the generated value type are excluded.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/backtracking_and_reversible_state c++20
```

Runtime checks should compare exhaustive small outputs and verify input restoration, duplicate suppression, and known queen counts.
