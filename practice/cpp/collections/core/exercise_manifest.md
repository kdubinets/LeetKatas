# Exercise Manifest

This manifest tracks each exercise's batch and primary implementation objective. The primary-skill column is intended to expose overlap; secondary topics describe supporting mechanics rather than additional learner tasks.

## Batch 1

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `append_vector_values` | Append an iterator range to a vector | Iterators, const source |
| `check_all_strings_nonempty` | Test whether all elements match a predicate | Ranges, strings, lambda |
| `check_unordered_map_membership` | Test unordered-map key membership | Const lookup, strings |
| `clamp_to_range` | Clamp a scalar to inclusive bounds | Standard utilities |
| `count_even_values` | Count elements matching a predicate | Ranges, lambda, count conversion |
| `drain_stack_to_vector` | Repeatedly read and pop a stack | Stack, vector |
| `erase_negative_map_values` | Erase map entries during iteration | Iterator validity, ordered map |
| `erase_odd_vector_values` | Erase vector elements matching a predicate | Sequence mutation, lambda |
| `find_first_long_string` | Find the first predicate match | Optional result, captured lambda |
| `find_smallest_with_min_heap` | Configure and construct a min-heap | Priority queue, comparator |
| `increment_frequency_count` | Increment an inserting mapped value | Unordered map, strings |
| `initialize_integer_grid` | Construct a filled two-dimensional vector | Nested vectors, sizes |
| `insert_map_default_if_absent` | Insert a map entry only when absent | Conditional insertion result |
| `insert_unordered_set_value` | Insert a unique value and report novelty | Unordered set, insertion result |
| `lower_bound_index` | Find the first value not less than a target | Binary-search boundary, iterator index |
| `make_ordered_set` | Construct a set from an iterator range | Deduplication, ordering |
| `maximum_array_value` | Find the maximum range element | Fixed array, iterator dereference |
| `pop_queue_front` | Safely read and remove a queue front | Optional result, queue |
| `push_priority_entry` | Construct a structured heap entry in place | Priority queue, pair |
| `read_map_value_without_insertion` | Retrieve a mapped value without insertion | Ordered map, optional result |
| `remove_adjacent_duplicates` | Compact and erase adjacent duplicates | Unique range, vector erasure |
| `rotate_vector_left` | Rotate a sequence left once | Empty-input guard, ranges |
| `sort_pairs_by_score_then_id` | Sort by a two-field custom ordering | Comparator, pairs, strict ordering |
| `sort_vector_ascending` | Sort a complete mutable range | Vector, ranges |
| `stable_partition_negatives` | Stably partition by a predicate | Vector, lambda |
| `substring_after_delimiter` | Extract text after the first delimiter | String search, substring |
| `sum_integer_values` | Accumulate into a widened numeric type | Numeric algorithm, type choice |
| `transform_to_lengths` | Transform strings into their lengths | Output iterator, reserved vector |
| `tuple_manhattan_distance` | Unpack a tuple with structured bindings | Tuple, absolute values |
| `weighted_sum_map_entries` | Iterate key-value bindings and aggregate | Ordered map, widened arithmetic |

## Batch 2

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `adjacent_duplicate_index` | Locate the first adjacent equal pair | Optional index, iterator conversion |
| `append_strings_by_moving` | Append a range through move iterators | Strings, moved-from state |
| `binary_search_sorted_vector` | Test membership in a sorted range | Binary search, const vector |
| `build_prefix_sums` | Produce inclusive prefix sums | Numeric scan, widened output |
| `check_any_value_exceeds_limit` | Test whether any element matches | Captured lambda, ranges |
| `check_string_prefix` | Test a string-view prefix | String view, C++20 string API |
| `collect_ordered_map_keys` | Extract keys in map iteration order | Map iteration, reserved vector |
| `compare_vectors_for_equality` | Compare complete ranges for equality | Length and element comparison |
| `copy_positive_values` | Copy matching values into a new range | Predicate copy, output iterator |
| `erase_set_value_range` | Erase an ordered value interval | Set boundaries, iterator range |
| `exchange_integer_value` | Replace a value while returning its old value | Utility operation, references |
| `fill_fixed_array` | Fill a fixed range with one value | Array, ranges |
| `find_all_target_indices` | Iterate safely with indices | Size types, result collection |
| `find_lowest_score_record` | Select an extremum through a projection | Records, member pointer |
| `find_map_entry_at_or_after_key` | Find an ordered-map key boundary | Optional pair, const lookup |
| `find_minimum_and_maximum` | Obtain both range extrema | Pair result, structured result |
| `find_partition_boundary` | Locate a predicate partition point | Iterator index, ranges |
| `first_mismatch_index` | Locate the first difference between ranges | Unequal lengths, optional index |
| `intersect_sorted_vectors` | Compute a sorted multiset intersection | Duplicate counts, output iterator |
| `make_zero_based_indices` | Generate consecutive numeric values | Size type, pre-sized vector |
| `merge_frequency_maps` | Add one frequency map into another | Structured bindings, intentional insertion |
| `merge_sorted_vectors` | Merge two sorted ranges | Reserved output, duplicates |
| `optional_value_or_fallback` | Consume an optional with a default | Const optional |
| `reverse_vector_subrange` | Reverse a validated indexed subrange | Iterator offsets, half-open range |
| `select_kth_smallest_in_place` | Place and retrieve an order statistic | Partial rearrangement, index conversion |
| `sort_records_by_id_projection` | Sort records through a member projection | Ranges, records |
| `split_string_on_delimiter` | Split while preserving empty fields | Repeated search, substrings |
| `unzip_pairs` | Decompose pairs into parallel vectors | Structured bindings, reserved outputs |
| `uppercase_ascii_string` | Transform characters in place | ASCII rules, lambda |
| `upper_bound_index` | Find the first value greater than a target | Binary-search boundary, iterator index |

## Batch 3

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `build_adjacent_differences` | Produce differences between neighboring values | Numeric algorithm, widened subtraction |
| `build_exclusive_prefix_sums` | Produce exclusive prefix sums | Numeric scan, widened output |
| `check_no_negative_values` | Test that no elements match a predicate | Ranges, lambda |
| `check_vector_sorted` | Verify nondecreasing range order | Const vector, ranges |
| `deduplicate_preserving_order` | Remove repeats while retaining first-occurrence order | Unordered set, output construction |
| `difference_sorted_vectors` | Compute a sorted multiset difference | Duplicate counts, output iterator |
| `dot_product_long_long` | Compute a widened inner product | Paired ranges, typed multiplication |
| `drain_priority_queue_descending` | Consume a heap into priority order | Intentional copy, repeated heap removal |
| `drop_string_view_prefix` | Advance a non-owning view boundary | String view, validated size |
| `equal_value_range_indices` | Find both boundaries of equal sorted values | Pair result, iterator indices |
| `erase_unordered_map_key` | Erase an associative entry by key | Unordered map, erase count |
| `erase_vector_value_at_index` | Erase a sequence element by index | Iterator offset, vector mutation |
| `find_subsequence_index` | Search for one contiguous range inside another | Optional index, empty pattern |
| `greatest_common_divisor_of_values` | Fold a range with greatest common divisor | Numeric utility, empty identity |
| `insert_or_assign_map_value` | Insert or overwrite an associative value | Ordered map, insertion result |
| `insert_vector_value_at_index` | Insert a sequence element by index | Iterator offset, append boundary |
| `join_strings_with_delimiter` | Join strings with separators only between elements | Indexed iteration, string building |
| `lexicographical_vector_compare` | Compare ranges lexicographically | Prefix ordering, const vectors |
| `parse_integer_exactly` | Parse an integer with complete-consumption validation | Character conversion, optional error result |
| `partial_sort_smallest_prefix` | Sort only the smallest prefix | Iterator boundary, partial ordering |
| `partition_copy_even_odd` | Split one input into two stable outputs | Pair of vectors, output iterators |
| `replace_first_substring` | Search and replace one bounded substring | Mutable string, success result |
| `replace_vector_value` | Replace all equal values in a range | Vector mutation, ranges |
| `resize_vector_with_value` | Resize a sequence with a growth value | Size type, shrinking and growth |
| `reverse_copy_with_view` | Materialize reverse traversal into a new vector | Reverse view, output iterator |
| `square_first_values_view` | Compose bounded and transforming views | Lazy pipeline, widened arithmetic |
| `sum_positive_values_view` | Filter lazily before accumulation | Filter view, widened sum |
| `sum_tuple_with_apply` | Expand tuple elements into a callable | Tuple utility, lambda |
| `swap_vector_contents` | Exchange complete container contents | Standard utility, constant-time swap |
| `union_sorted_vectors` | Compute a sorted multiset union | Duplicate counts, output iterator |

## Batch 4

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `add_to_all_map_values` | Mutate mapped values without changing keys | Ordered map, entry mutability |
| `add_vectors_elementwise` | Transform two ranges into corresponding sums | Binary transformation, widened arithmetic |
| `advance_to_next_permutation` | Advance and report a lexicographical permutation | Result object, sequence mutation |
| `check_sorted_multiset_includes` | Test multiplicity-aware sorted containment | Two sorted ranges, const inputs |
| `check_vector_permutation` | Compare unordered element multiplicities | Whole-range permutation check |
| `configure_structured_min_heap` | Define structured min-heap ordering | Custom comparator, tie-breaking |
| `copy_smallest_values_sorted` | Partially sort into a separate bounded output | Const input, sized destination |
| `count_set_bits` | Count one bits in an unsigned integer | C++20 bit utility |
| `erase_one_multiset_occurrence` | Erase exactly one matching duplicate | Multiset, iterator erasure |
| `find_set_value_position` | Measure a non-random-access iterator position | Ordered set, optional index |
| `generate_arithmetic_progression` | Generate values with mutable lambda state | Initialized capture, representable arithmetic |
| `inplace_merge_sorted_halves` | Merge adjacent sorted regions in place | Iterator boundary, vector mutation |
| `insert_into_sorted_vector` | Preserve ordering during sequence insertion | Binary-search boundary, iterator insertion |
| `safe_integer_midpoint` | Compute an overflow-safe integer midpoint | C++20 numeric utility, rounding direction |
| `shift_fixed_array_right` | Copy safely across an overlapping range | Backward copying, fixed array |
| `stable_sort_records_by_group` | Preserve tie order during record sorting | Stable sort, member projection |
| `take_and_erase_map_value` | Move out a mapped value and erase its entry | Optional result, iterator safety |
| `trim_ascii_whitespace_view` | Narrow a view around non-whitespace content | String view, all-whitespace case |
