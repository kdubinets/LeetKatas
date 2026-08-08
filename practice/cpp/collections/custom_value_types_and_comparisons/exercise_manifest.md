# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `default_value_equality` | Generate memberwise equality for a value type | Defaulted hidden-friend operator |
| `custom_value_equality` | Define equality from the identity-bearing fields of a value type | Ignored metadata field |
| `symmetric_scalar_equality` | Support symmetric equality between a value type and its scalar representation | Hidden friend, rewritten candidates |
| `default_three_way_comparison` | Generate lexicographic ordering and equality for a value type | Defaulted spaceship |
| `compare_strong_value` | Implement a strong three-way comparison from one canonical field | `strong_ordering` |
| `symmetric_scalar_ordering` | Support symmetric ordering between a value type and its scalar representation | Rewritten relational candidates |
| `compare_case_insensitive_text` | Implement a weak ordering for case-insensitive text | Equivalent spellings, `weak_ordering` |
| `compare_floating_value` | Expose the partial ordering of a floating-point value type | Unordered NaN state |
| `compare_semantic_version` | Compose a three-field lexicographic comparison | Tuple comparison |
| `compare_by_distance_then_point` | Define a total strict ordering with a computed primary key and tie-breakers | Ordered key policy |
| `use_comparison_category` | Test whether a three-way comparison result is less than zero | Comparison-category utilities |
| `find_equivalent_set_value` | Find an element through comparator equivalence | Ordered set, non-equality equivalence |
| `define_transparent_comparator` | Define one ordering policy for stored and alternate lookup keys | Transparent comparator, string view |
| `heterogeneous_set_lookup` | Look up a custom set key using a non-owning alternate type | Transparent comparator, string view |
| `heterogeneous_map_lookup` | Read a custom-keyed map using a scalar alternate key | Transparent comparator, optional result |
| `change_ordered_map_key` | Replace an ordered custom key without copying its mapped value | Node handle, key immutability |
| `hash_custom_value` | Combine hashes for all equality-bearing fields | Unordered key support |
| `equal_custom_value` | Define the equality policy paired with a custom hash | Hash/equality consistency |
| `hash_case_insensitive_text` | Hash normalized text consistently with case-insensitive equality | Equality/hash contract, ASCII folding |
| `specialize_hash_for_value` | Provide the standard hash specialization for a user-defined type | Default unordered-container policy |
| `define_transparent_unordered_policies` | Define matching transparent hash and equality policies | Allocation-free heterogeneous lookup |
