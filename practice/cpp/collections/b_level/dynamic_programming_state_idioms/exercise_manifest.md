# Exercise Manifest

Primary skills identify distinct state-storage or dependency-order invariants. Supporting recurrence mechanics are not separate learner tasks.

## Batch 1

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `maximum_nonadjacent_sum_rolling` | Preserve two prior recurrence states during a linear scan | Empty selection, widened sums |
| `count_grid_paths_rolling_row` | Update one row from its prior-row and current-row-left dependencies | Grid boundary state, positive dimensions |
| `maximum_zero_one_capacity_value` | Update capacities in descending order so each item contributes at most once | Zero-one choice, exact update boundary |

## Batch 2

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `count_unordered_coin_combinations` | Update amounts in ascending order while each coin remains reusable | Combination order, zero target |
| `longest_common_subsequence_rolling` | Preserve the overwritten prior diagonal during an in-place row update | Two-sequence recurrence, empty input |
| `minimum_step_cost_memoized` | Distinguish uncomputed cache entries from valid zero-valued results | Top-down recurrence, terminal states |

## Batch 3

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `minimum_coin_count_with_sentinel` | Minimize only from reachable states using an explicit sentinel | Reusable coins, optional impossible result |
| `maximum_profit_state_machine` | Derive coupled next states from the same prior snapshot | Holding and cash states, transaction fee |
| `longest_increasing_subsequence_quadratic` | Aggregate over all valid predecessor states | Per-index base state, strict comparison |
| `minimum_falling_path_two_rows` | Rotate distinct rows with bounded prior-row dependencies | Edge columns, widened sums |
