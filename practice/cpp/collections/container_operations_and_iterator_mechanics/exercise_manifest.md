# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `add_deque_end_values` | Add specified values at the front and back of a deque | `push_front`, `push_back` |
| `take_deque_end_values` | Read and remove both endpoint values from a deque containing at least two elements | `front`, `back`, endpoint erasure |
| `sort_list_values` | Sort a list through its container-owned stable operation | Bidirectional iterators, node relinking |
| `merge_sorted_lists` | Merge two ascending lists by transferring nodes | Linear merge, stable equivalent values |
| `splice_all_list_nodes` | Transfer every node from one list into another at a supplied position | `list::splice`, iterator stability |
| `splice_list_node_range` | Transfer a supplied half-open node range between lists | Range splice, no element moves |
| `remove_matching_list_values` | Remove predicate-matching list nodes and return the C++20 removal count | `list::remove_if` |
| `deduplicate_adjacent_list_values` | Collapse adjacent equal list values and return the C++20 removal count | `list::unique` |
| `insert_after_forward_list_predecessor` | Insert a value after a supplied forward-list predecessor | `before_begin`, `insert_after` |
| `erase_after_forward_list_predecessor` | Erase the node after a supplied forward-list predecessor | `erase_after`, returned successor |
| `splice_after_forward_list_predecessor` | Transfer one forward-list node after supplied source and destination predecessors | `splice_after`, iterator stability |
| `insert_after_forward_list_head` | Insert a range after the conceptual position before a forward list's first node | `before_begin`, range `insert_after` |
| `collect_multimap_key_values` | Retrieve every mapped value associated with one multimap key | `equal_range`, duplicate keys |
| `merge_unique_map_nodes` | Transfer non-colliding map nodes while retaining source collisions | Associative `merge` |
| `reserve_unordered_map_for_insertions` | Reserve capacity for a known final unordered-map size before bulk insertion | Rehash avoidance, range insertion |
| `advance_list_iterator` | Move a list iterator forward by a validated runtime distance | `std::advance`, bidirectional iterator |
| `copy_with_front_inserter` | Copy values into an existing forward list through front insertion | `front_inserter`, reversed inserted prefix |
| `insert_with_positional_inserter` | Insert transformed output before a stable list position through a general insertion adaptor | `inserter`, ranges transform |
| `materialize_reverse_iterators` | Construct an owning result through a container's reverse iterators | Legacy iterator-pair interface |
| `erase_at_reverse_iterator` | Convert a reverse position to the corresponding forward erase position | Reverse-iterator base offset, returned successor |
| `copy_unique_values_with_progress` | Consume both iterator fields from a C++20 ranges unique-copy result | Adjacent runs, differing input and output progress |
| `move_value_through_iterator` | Move a value through an iterator customization point in generic code | `ranges::iter_move`, proxy-aware access |
| `swap_values_through_iterators` | Exchange values through iterator customization points | `ranges::iter_swap` |
