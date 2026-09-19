# Exercise Manifest

Primary skills identify distinct link invariants rather than different problem stories. Supporting mechanics are not separate tasks.

## Batch 1

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `reverse_entire_list` | Preserve the unprocessed suffix while reversing a chain | New head, null termination |
| `remove_matching_nodes` | Maintain the predecessor of the next candidate across consecutive removals | Dummy head, caller-owned excluded nodes |
| `merge_sorted_node_chains` | Maintain one output tail while consuming two disjoint sorted chains | Stable equality rule, exhausted input |

## Batch 2

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `stable_partition_nodes_by_sign` | Maintain two stable output chains and join them without stale links | Two tails, explicit null termination |
| `swap_adjacent_node_pairs` | Reconnect repeated two-node blocks across a stable prefix boundary | Dummy head, odd final node |
| `reverse_node_segment` | Preserve and reconnect both outer boundaries of a reversed segment | Fixed predecessor, inclusive zero-based positions |
