# Partition and Selection Idioms

## Status

Active provisional Level B compact module designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

The initial set contains the two distinct objectives supported by the roadmap. Reassessment found no quality addition: binary predicate partition already exists in sequence scanning, zero-one-two variants repeat three-way regions, and additional order-statistic stories repeat range shrinking.

## Contract

The pivot, region invariant, equality rule, and partition helper are supplied. Learners implement either region transitions or selection-range transitions, not both in one exercise.

## Included State Shapes

- Maintain less-than, equal, unknown, and greater-than regions around a supplied pivot value.
- Shrink an inclusive candidate range from the final pivot position returned by supplied partition machinery.

## Exclusions

Pivot-strategy design, randomized performance analysis, stable partitioning, full sorting, standard-library selection calls, and duplicate story variants are excluded.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/partition_and_selection_idioms c++20
```

Runtime checks should exhaust small arrays with duplicates, verify region membership and multiplicity, and compare every requested rank with sorted results.
