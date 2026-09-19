# Exercise Collections

Each Level A exercise collection lives in its own descriptively named subdirectory. The completed [core collection](core/collection_spec.md) establishes the baseline layout; focused Level A follow-up collections live alongside it. Level B interview-idiom collections live beneath [b_level](b_level/README.md) so their supplied-pattern practice remains distinct from Level A API fluency.

## Available Collections

- [Core](core/collection_spec.md): 108 general implementation-fluency exercises, up to C++20.
- [Non-Owning Views and Ranges](non_owning_views_and_ranges/collection_spec.md): 30 focused Level A exercises, up to C++20.
- [Ownership, Move Semantics, and RAII](ownership_move_semantics_and_raii/collection_spec.md): 36 focused Level A exercises, up to C++20.
- [Templates and Concepts](templates_and_concepts/collection_spec.md): 36 focused Level A exercises, up to C++20.
- [Text Processing and Conversion](text_processing_and_conversion/collection_spec.md): 28 focused Level A exercises, up to C++20.
- [Numeric and Bit Manipulation](numeric_and_bit_manipulation/collection_spec.md): 26 focused Level A exercises, up to C++20.
- [Variants and Error Modelling](variants_and_error_modelling/collection_spec.md): 21 focused Level A exercises, up to C++20.
- [Custom Value Types and Comparisons](custom_value_types_and_comparisons/collection_spec.md): 21 focused Level A exercises, up to C++20.
- [Callable Utilities](callable_utilities/collection_spec.md): 20 focused Level A exercises, up to C++20.
- [Chrono](chrono/collection_spec.md): 36 focused Level A exercises, up to C++20.
- [Filesystem](filesystem/collection_spec.md): 37 focused Level A exercises, up to C++20.
- [C++20 Language Features](cpp20_language_features/collection_spec.md): 15 focused Level A C++20 language-delta exercises.
- [Concurrency](concurrency/collection_spec.md): 37 focused Level A exercises, up to C++20.
- [Compile-Time Programming](compile_time_programming/collection_spec.md): 18 focused Level A exercises, up to C++20.
- [Stream and File I/O](stream_and_file_io/collection_spec.md): 20 focused Level A exercises, up to C++20.
- [Container Operations and Iterator Mechanics](container_operations_and_iterator_mechanics/collection_spec.md): 23 focused Level A exercises, up to C++20.
- [Sequence Scanning and Window Idioms](b_level/sequence_scanning_and_window_idioms/collection_spec.md): 19 Level B named interview-implementation idioms, up to C++20.
- [Linked-List Pointer Rewiring](b_level/linked_list_pointer_rewiring/collection_spec.md): six provisional Level B node-link idioms, up to C++20; not corpus-audited.
- [Dynamic Programming State Idioms](b_level/dynamic_programming_state_idioms/collection_spec.md): ten provisional Level B supplied-recurrence idioms, up to C++20; not corpus-audited.
- [Monotonic Stack and Deque Idioms](b_level/monotonic_stack_and_deque_idioms/collection_spec.md): seven provisional Level B ordered-candidate idioms, up to C++20; not corpus-audited.
- [Tree Traversal and Recursive State](b_level/tree_traversal_and_recursive_state/collection_spec.md): six provisional Level B tree-state idioms, up to C++20; not corpus-audited.
- [Graph Traversal and Visitation](b_level/graph_traversal_and_visitation/collection_spec.md): six provisional Level B graph-state idioms, up to C++20; not corpus-audited.
- [Interval Merging and Sweep Events](b_level/interval_merging_and_sweep_events/collection_spec.md): four provisional Level B interval-state idioms, up to C++20; not corpus-audited.
- [Heap Frontier and Streaming State](b_level/heap_frontier_and_streaming_state/collection_spec.md): four provisional Level B heap-state idioms, up to C++20; not corpus-audited.
- [Disjoint-Set Connectivity Bookkeeping](b_level/disjoint_set_connectivity_bookkeeping/collection_spec.md): three provisional Level B union-find idioms, up to C++20; not corpus-audited.
- [Backtracking and Reversible State](b_level/backtracking_and_reversible_state/collection_spec.md): six provisional Level B choice-restoration idioms, up to C++20; not corpus-audited.
- [Partition and Selection Idioms](b_level/partition_and_selection_idioms/collection_spec.md): two provisional Level B region/selection idioms, up to C++20; not corpus-audited.

## Required Collection Files

```text
collections/<collection_name>/              # Level A
collections/b_level/<collection_name>/      # Level B
├── collection.json              # optional stable identity for progress sync
├── environment.json             # optional machine-readable target environment
├── collection_spec.md
├── exercise_manifest.md
├── <exercise_name>.cpp
└── <exercise_name>.md
```

The collection specification must define:

- Purpose and learner level.
- Target language boundary, including whether it is up-to-version or version-delta.
- Expected exercise granularity.
- Included and excluded topic families.
- Validation standard and any toolchain requirements.
- Current status: planned, active, or frozen.

The manifest must identify each exercise's primary skill clearly enough to detect overlap.

An optional `collection.json` makes scheduler history portable across checkout
paths and enables progress synchronization. It contains only a schema version
and a globally stable collection ID:

```json
{
  "schema_version": 1,
  "id": "leetkatas.cpp.core"
}
```

Do not change an ID after publishing a collection. A missing or malformed file
leaves the collection fully usable as local-only practice.

An optional `environment.json` supplies the target language version, available
libraries, and restrictions to the evaluation harness and reviewer. It describes
what is available, not what an exercise must use; technique requirements belong
in the exercise metadata. For example:

```json
{
  "language": {
    "name": "C++",
    "version": "C++20"
  },
  "libraries": [
    {
      "name": "C++ standard library",
      "version": "C++20"
    }
  ],
  "restrictions": [
    "No third-party libraries"
  ]
}
```

`language.name` and `language.version` are required non-empty strings.
`implementation` may optionally identify a runtime or compiler, while
`libraries` and `restrictions` are optional arrays. Library entries require a
name and may include a version.

An optional `exercise_order.md` defines a canonical introduction order. It must
contain every exercise basename exactly once, one unadorned basename per line.

Use [CppFollowUpTopics.md](../CppFollowUpTopics.md) to select and prioritize future collections.
