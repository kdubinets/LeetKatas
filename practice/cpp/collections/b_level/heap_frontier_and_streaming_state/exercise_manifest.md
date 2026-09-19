# Exercise Manifest

## Initial Batch

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `merge_k_sorted_sequences` | Replace each popped frontier entry with its successor from the same input | Structured heap entries, exhausted inputs |
| `retain_k_smallest_values` | Keep a reversed heap bounded to the best k values seen | Duplicate values, sorted result |
| `dijkstra_shortest_distances` | Skip stale distance entries and relax outgoing weighted edges | Optional distances, nonnegative weights |
| `running_stream_medians` | Preserve ordering and size balance between lower and upper heaps | Even prefix average, widened addition |

## Reassessment

No additions: plausible remaining candidates duplicate interval concurrency, bounded top-k state, or Level A heap operations.
