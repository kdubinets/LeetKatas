# Exercise Manifest

## Initial Batch

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `merge_sorted_closed_intervals` | Extend or emit one active interval while scanning sorted starts | Inclusive overlap, nested intervals |
| `insert_closed_interval` | Transition through before, overlapping, and after regions around one inserted interval | Sorted disjoint input, endpoint equality |
| `intersect_sorted_closed_intervals` | Emit pairwise overlap and advance the interval ending first | Two sorted disjoint lists, inclusive endpoints |
| `minimum_half_open_meeting_rooms` | Apply end events before starts at equal times while tracking active count | Half-open meetings, maximum concurrency |

## Reassessment

No additions: remaining candidates duplicate these state shapes or belong to greedy selection or heap-frontier families.
