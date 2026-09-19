# Exercise Manifest

## Initial Batch

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `next_greater_indices` | Resolve pending indices when a strictly greater value arrives | Optional positions, duplicates |
| `previous_smaller_indices` | Remove non-smaller candidates before reading the nearest strict boundary | Equality rule, optional positions |
| `stock_span_lengths` | Convert a previous-greater boundary into an inclusive span | Decreasing index stack, equal prices |
| `sliding_window_maximum` | Expire old indices and discard dominated values in a decreasing deque | Fixed width, duplicate maxima |
| `largest_rectangle_area` | Propagate the earliest start while finalizing taller bars | Sentinel boundary, widened area |

## Reassessment Additions

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `smallest_digits_after_removal` | Maintain monotonic digits while consuming a bounded pop budget | Suffix removal, leading zero normalization |
| `shortest_subarray_at_least_target` | Apply distinct front-satisfaction and back-domination rules to prefix indices | Negative values, optional length |
