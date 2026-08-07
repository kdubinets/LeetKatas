# Exercise Manifest

The primary-skill column identifies the distinct implementation objective. Secondary topics are supporting mechanics rather than additional learner tasks.

| Exercise | Primary skill | Secondary topics |
|---|---|---|
| `construct_dynamic_span` | Construct a dynamic-extent span over a vector | Mutable borrowing, no copy |
| `construct_fixed_span` | Construct a fixed-extent const span over an array | Static extent, const borrowing |
| `take_span_prefix` | Select a runtime-sized span prefix | Dynamic subview |
| `take_fixed_span_suffix` | Select a compile-time-sized span suffix | Fixed extent |
| `select_fixed_span_subview` | Select a compile-time offset and count | Fixed subspan |
| `measure_span_bytes` | Measure a span in bytes | Element size |
| `view_span_as_bytes` | Expose object representations as const bytes | Read-only byte view |
| `view_span_as_writable_bytes` | Expose mutable object representations as bytes | Writable byte view |
| `view_vector_tail` | Return a span into a vector suffix | Owner lifetime, non-owning result |
| `span_from_first_match` | Return a borrowed span beginning at a found element | Borrowed iterator, subview |
| `remove_string_view_suffix` | Narrow a string view from its end | In-place view mutation |
| `consume_string_view_token` | Return one delimited token and advance input | Allocation-free incremental parsing |
| `consume_leading_digits_view` | Return one predicate-defined token and advance input | ASCII digits, allocation-free parsing |
| `view_after_last_delimiter` | Slice after the final delimiter | Reverse search, no copy |
| `consume_string_view_prefix` | Return and consume a fixed-width prefix | Paired prefix view operations |
| `materialize_range_window` | Compose offset and count views, then materialize | `drop`, `take`, C++20 copying |
| `materialize_until_negative` | Lazily select a predicate-defined prefix | `take_while` |
| `materialize_after_leading_zeroes` | Lazily discard a predicate-defined prefix | `drop_while` |
| `filter_and_transform_view` | Compose filtering and transformation | Lazy pipeline, materialization |
| `collect_map_keys_view` | Traverse associative keys through an element view | `views::keys` |
| `contains_map_value_view` | Search only mapped values through an element view | `views::values` |
| `flatten_nested_ranges` | Flatten nested ranges lazily | `views::join` |
| `split_string_view_fields` | Materialize non-owning fields from a split view | `views::split`, subranges |
| `make_bounded_iota_view` | Construct a finite integer iota view | Iterator/sentinel range |
| `materialize_infinite_iota_prefix` | Bound an unbounded iota view | Unreachable sentinel, `take` |
| `materialize_counted_range` | Traverse a counted iterator range | `views::counted` |
| `select_iterator_subrange` | Construct a subrange from indexed iterators | Borrowed iterator pair |
| `materialize_with_common_view` | Adapt differing iterator and sentinel types for iterator-pair construction | `views::common` |
| `return_lazy_scaled_view` | Return a transform view over caller-owned data | Captured state, lifetime contract |
| `own_rvalue_range_view` | Turn transferred storage into an owning all-view | Lifetime safety, `views::all` |
