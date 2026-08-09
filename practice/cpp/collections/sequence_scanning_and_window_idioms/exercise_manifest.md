# Exercise Manifest

The primary-skill column identifies one named idiom and its distinct state-management objective. Supporting mechanics are not separate learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `fixed_window_maximum_sum` | Maintain a rolling numeric total for a fixed-width window | Window entry and exit, widened arithmetic |
| `fixed_window_all_distinct_count` | Maintain fixed-window frequency state while counting valid windows | Frequency table, window size |
| `fixed_window_anagram_match_count` | Compare a fixed-width character-frequency state to a target state | Lowercase alphabet, rolling counts |
| `longest_unique_substring` | Shrink a window until every character count is at most one | Frequency invariant, best length |
| `minimum_length_sum_at_least_target` | Shrink a positive-sum window while it remains sufficient | Numeric invariant, minimum length |
| `longest_at_most_k_distinct` | Restore a distinct-key limit by advancing the left boundary | Frequency table, key removal |
| `two_sum_sorted_converging` | Move converging sorted-sequence pointers according to the sum comparison | Optional index pair, ordered input |
| `maximum_container_area` | Discard the dominated endpoint after measuring a two-pointer pair | Width calculation, bounded heights |
| `merge_sorted_sequences_from_end` | Merge two sorted sequences backwards into reserved output space | In-place writes, exhaustion handling |
| `compact_sorted_duplicates` | Use read/write pointers to retain one representative of each run | In-place compaction, returned length |
| `move_zeroes_in_place` | Use read/write pointers to stably compact selected values | In-place swaps, relative order |
| `partition_negatives_first` | Partition a sequence with opposing pointers and return the boundary | Unstable partitioning, endpoint movement |
| `count_subarrays_with_target_sum` | Count target-sum subarrays from prior prefix frequencies | Prefix sum, occurrence map |
| `longest_balanced_binary_subarray` | Retain the earliest prefix position for each balance to maximize an equal-zero-one span | Balance transform, prefix-position distance |
| `range_sum_queries_from_prefixes` | Answer inclusive range sums using a one-past prefix representation | Prefix indexing, batch queries |
| `apply_closed_range_additions` | Record closed range updates in a difference array before materializing values | Boundary cancellation, running total |
| `binary_search_exact` | Maintain a half-open candidate interval for exact manual binary search | Safe midpoint, optional result |
| `binary_search_first_not_less` | Maintain the first position satisfying a monotone lower boundary | Half-open interval, insertion position |
| `binary_search_last_not_greater` | Derive the last position satisfying an upper boundary from a half-open interval | Empty result, one-past boundary |
