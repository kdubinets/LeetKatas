# Disjoint-Set Connectivity Bookkeeping

## Status

Active provisional Level B compact module designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

The initial set contains three exercises. Reassessment found no fourth objective that was not a story variant or a whole connectivity problem. Compactness is intentional.

## Contract

The parent-forest representation and root/size preconditions are supplied. Exercises isolate path shortening, weighted root attachment, and successful-union counting. They do not ask learners to invent or implement a complete data structure.

## Included State Shapes

- Follow parent links while shortening the queried path.
- Attach the smaller distinct root under the larger and update only the surviving size.
- Decrement a running component count only when a supplied union changes connectivity.

## Exclusions

Rank-versus-size symmetry, redundant recursive-find variants, rollback DSU, offline dynamic connectivity, account-merging stories, and complete class design are excluded.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/disjoint_set_connectivity_bookkeeping c++20
```

Runtime checks should compare connectivity partitions, root sizes, path validity, and component-count sequences under repeated and self connections.
