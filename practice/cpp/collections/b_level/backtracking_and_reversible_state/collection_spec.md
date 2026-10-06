# Backtracking and Reversible State

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

Four initial exercises cover path restoration, used-marker restoration, reusable-choice pruning, and temporary grid mutation. Reassessment retained same-depth duplicate suppression and coordinated occupancy sets because they add distinct reversible-state decisions.

## Contract

The choice order, stopping condition, pruning rule, and state meaning are supplied. Learners implement one choose/recurse/undo invariant in 3–8 minutes rather than discover a search formulation. Output order is specified when observable.

Each learner source supplies only the public entry function with a pattern hint and one Finish comment describing the complete task. Recursive helpers, state storage, initialization, and traversal belong to the learner's implementation.

## Included State Shapes

- Append and remove one path choice around recursion.
- Mark and unmark a distinct input position.
- Reuse a sorted candidate while reducing a remaining target.
- Temporarily mark a grid cell and restore it on every return path.
- Skip equal values only when they compete at the same search depth.
- Apply and undo one queen across three coupled occupancy tables.

## Exclusions

Tree traversal over an existing structure, graph visitation, unconstrained exponential puzzles, solver frameworks, and variants changing only the generated value type are excluded.

## Future Candidate

The first candidate for a seventh exercise is permutation generation by in-place swapping. Maintain a fixed prefix and an available-choice suffix; swap each candidate into the next prefix position, recurse, and undo the swap. The input must be exactly restored on return. This trains restoration of rearranged state, a different state shape from the existing permutation exercise's shared path and used-position markers.

Keep the current six exercises as the provisional core. This candidate is recorded for future reassessment, not approved for addition or supported by corpus evidence. Before adding it, confirm that it offers a distinct 3–8 minute implementation objective and specify output order and input-restoration requirements in the entry function's Finish comment.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/backtracking_and_reversible_state c++20
```

Runtime checks should compare exhaustive small outputs and verify input restoration, duplicate suppression, and known queen counts.
