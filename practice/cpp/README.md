# C++ Exercise Collections

This directory contains focused C++ practice collections and the documentation used to grow and validate them.

## Layout

```text
cpp/
├── AGENTS.md
├── README.md
├── CppFollowUpTopics.md
├── CppProblemsGenerationPrompt.md
├── LevelBInterviewIdiomsPlan.md
├── collections/
│   ├── README.md
│   ├── core/
│   │   ├── collection.json
│   │   ├── collection_spec.md
│   │   ├── environment.json
│   │   ├── exercise_manifest.md
│   │   ├── exercise_order.md
│   │   └── 108 exercise pairs
│   ├── b_level/
│   │   ├── sequence_scanning_and_window_idioms/
│   │   │   └── 19 Level B exercise pairs plus collection metadata
│   │   ├── linked_list_pointer_rewiring/
│   │   │   └── 6 Level B exercise pairs plus collection metadata
│   │   ├── dynamic_programming_state_idioms/
│   │   │   └── 10 Level B exercise pairs plus collection metadata
│   │   ├── monotonic_stack_and_deque_idioms/
│   │   │   └── 7 Level B exercise pairs plus collection metadata
│   │   ├── tree_traversal_and_recursive_state/
│   │   │   └── 6 Level B exercise pairs plus collection metadata
│   │   ├── graph_traversal_and_visitation/
│   │   │   └── 6 Level B exercise pairs plus collection metadata
│   │   ├── interval_merging_and_sweep_events/
│   │   │   └── 4 Level B exercise pairs plus collection metadata
│   │   ├── heap_frontier_and_streaming_state/
│   │   │   └── 4 Level B exercise pairs plus collection metadata
│   │   ├── disjoint_set_connectivity_bookkeeping/
│   │   │   └── 3 Level B exercise pairs plus collection metadata
│   │   ├── backtracking_and_reversible_state/
│   │   │   └── 6 Level B exercise pairs plus collection metadata
│   │   └── partition_and_selection_idioms/
│   │       └── 2 Level B exercise pairs plus collection metadata
│   ├── non_owning_views_and_ranges/
│   │   └── 30 exercise pairs plus collection metadata
│   ├── ownership_move_semantics_and_raii/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── templates_and_concepts/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── text_processing_and_conversion/
│   │   └── 28 exercise pairs plus collection metadata
│   ├── numeric_and_bit_manipulation/
│   │   └── 26 exercise pairs plus collection metadata
│   ├── variants_and_error_modelling/
│   │   └── 21 exercise pairs plus collection metadata
│   ├── custom_value_types_and_comparisons/
│   │   └── 21 exercise pairs plus collection metadata
│   ├── callable_utilities/
│   │   └── 20 exercise pairs plus collection metadata
│   ├── chrono/
│   │   └── 36 exercise pairs plus collection metadata
│   ├── filesystem/
│   │   └── 37 exercise pairs plus collection metadata
│   ├── cpp20_language_features/
│   │   └── 15 exercise pairs plus collection metadata
│   ├── concurrency/
│   │   └── 37 exercise pairs plus collection metadata
│   ├── compile_time_programming/
│   │   └── 18 exercise pairs plus collection metadata
│   ├── stream_and_file_io/
│   │   └── 20 exercise pairs plus collection metadata
│   └── container_operations_and_iterator_mechanics/
│       └── 23 exercise pairs plus collection metadata
└── tools/
    └── validate_exercises.sh
```

## Current Collections

The [core collection](collections/core/collection_spec.md) contains 108 Level A implementation-fluency exercises targeting idiomatic C++ up to and including C++20. It is considered complete and should normally remain frozen.

Fifteen focused up-to-C++20 follow-up collections are also complete:

- [Non-Owning Views and Ranges](collections/non_owning_views_and_ranges/collection_spec.md) contains 30 exercises on spans, string views, lazy composition, iterator/sentinel ranges, borrowing, and materialization.
- [Ownership, Move Semantics, and RAII](collections/ownership_move_semantics_and_raii/collection_spec.md) contains 36 exercises on smart pointers, ownership transfer, moved-from states, rule-of-zero composition, move-aware handles, and deterministic cleanup.
- [Templates and Concepts](collections/templates_and_concepts/collection_spec.md) contains 36 exercises on template forms, dependent names, packs, traits, compile-time branching, requires-expressions, named concepts, and constrained overloads.
- [Text Processing and Conversion](collections/text_processing_and_conversion/collection_spec.md) contains 28 exercises on character conversion, streams, regular-expression APIs, and C++20 formatting.
- [Numeric and Bit Manipulation](collections/numeric_and_bit_manipulation/collection_spec.md) contains 26 exercises on bit utilities, masks, safe numeric operations, reductions, and randomization.
- [Variants and Error Modelling](collections/variants_and_error_modelling/collection_spec.md) contains 21 exercises on variant state handling and visitation, optional composition, explicit value-or-error results, and error boundaries.
- [Custom Value Types and Comparisons](collections/custom_value_types_and_comparisons/collection_spec.md) contains 21 exercises on equality, three-way comparison categories, ordered key policies, heterogeneous lookup, and hashing contracts.
- [Callable Utilities](collections/callable_utilities/collection_spec.md) contains 20 exercises on type-erased callbacks, overload selection, uniform invocation, binding, reference wrappers, callable adaptors, and C++20 lambda forms.
- [Chrono](collections/chrono/collection_spec.md) contains 36 exercises on durations, time points, deadlines, civil calendars, calendar differences, weekdays, and time-of-day decomposition.
- [Filesystem](collections/filesystem/collection_spec.md) contains 37 exercises on lexical paths, status and mutation operations, error-code overloads, symbolic links, recursive copying, and directory traversal.
- [C++20 Language Features](collections/cpp20_language_features/collection_spec.md) contains 15 language-delta exercises on initialization, scoped names, conditional explicitness, lambda changes, UTF-8 types, attributes, and variadic preprocessing.
- [Concurrency](collections/concurrency/collection_spec.md) contains 37 exercises on thread lifetime, cooperative cancellation, locking, condition waits, atomics, coordination primitives, asynchronous results, shared locking, one-time initialization, and synchronized output.
- [Compile-Time Programming](collections/compile_time_programming/collection_spec.md) contains 18 exercises on constant-evaluable functions, representative algorithms, dynamic storage, validation, immediate functions, constant initialization, and C++20 constexpr object-model features.
- [Stream and File I/O](collections/stream_and_file_io/collection_spec.md) contains 20 exercises on line input, stream-state recovery, file modes, input and output positioning, bounded byte transfer, stream-buffer copying, and C++20 string-stream buffer views and moves.
- [Container Operations and Iterator Mechanics](collections/container_operations_and_iterator_mechanics/collection_spec.md) contains 23 exercises on deque endpoints, list sorting and node operations, forward-list operations, multimap ranges, associative node transfer, unordered capacity, iterator adaptors, ranges result objects, and iterator customization points.

The proposed Level B [Sequence Scanning and Window Idioms](collections/b_level/sequence_scanning_and_window_idioms/collection_spec.md) collection contains 19 named, supplied interview implementation patterns. It is intentionally not yet complete: a dedicated Level B corpus audit must evaluate it against solved interview solutions before it is frozen or extended.

The provisional Level B [Linked-List Pointer Rewiring](collections/b_level/linked_list_pointer_rewiring/collection_spec.md) collection contains six exercises on reversal, filtering, merging, stable partitioning, pair swapping, and segment boundaries. It was designed from general considerations, not corpus extraction, and is not complete or frozen. Recorded solutions have deterministic node-identity and topology checks in addition to compilation validation.

The provisional Level B [Dynamic Programming State Idioms](collections/b_level/dynamic_programming_state_idioms/collection_spec.md) collection contains ten supplied-recurrence exercises on rolling states, update direction, sentinels, coupled states, predecessor aggregation, row rotation, and memoization. It was designed from general considerations, not corpus extraction, and is not complete or frozen.

The provisional Level B [Monotonic Stack and Deque Idioms](collections/b_level/monotonic_stack_and_deque_idioms/collection_spec.md) collection contains seven exercises on unresolved indices, strict boundaries, spans, deque expiration, histogram boundaries, bounded greedy popping, and prefix candidates. It was designed from general considerations and is not corpus-audited or frozen.

The provisional Level B [Tree Traversal and Recursive State](collections/b_level/tree_traversal_and_recursive_state/collection_spec.md) collection contains six exercises on postorder summaries, ancestor context, path accumulators, explicit traversal suspension, and node-result propagation. It was designed from general considerations and is not corpus-audited or frozen.

The provisional Level B [Graph Traversal and Visitation](collections/b_level/graph_traversal_and_visitation/collection_spec.md) collection contains six exercises on discovery timing, components, coloring, indegrees, multi-source initialization, and active traversal state. It was designed from general considerations and is not corpus-audited or frozen.

The provisional Level B [Interval Merging and Sweep Events](collections/b_level/interval_merging_and_sweep_events/collection_spec.md) collection contains four exercises on active closed intervals, insertion phases, paired interval frontiers, and equal-time event ordering. The separate [Heap Frontier and Streaming State](collections/b_level/heap_frontier_and_streaming_state/collection_spec.md) collection contains four exercises on multi-sequence frontiers, bounded retention, stale distance entries, and balanced stream halves. Both were designed from general considerations and remain provisional.

The provisional Level B [Disjoint-Set Connectivity Bookkeeping](collections/b_level/disjoint_set_connectivity_bookkeeping/collection_spec.md) compact module contains three exercises on path halving, union by size, and successful-union component counts. It was designed from general considerations and is not corpus-audited or frozen.

The provisional Level B [Backtracking and Reversible State](collections/b_level/backtracking_and_reversible_state/collection_spec.md) collection contains six exercises on path, marker, grid, duplicate, and coupled-constraint restoration. The compact [Partition and Selection Idioms](collections/b_level/partition_and_selection_idioms/collection_spec.md) module contains two exercises on three-way regions and quickselect range shrinking. Both were designed from general considerations and remain provisional.

The core [exercise order](collections/core/exercise_order.md) records the canonical
1-to-108 progression as one exercise basename per line. The
[exercise manifest](collections/core/exercise_manifest.md) records generation
batch, primary implementation skill, and supporting topics.

## Planning Documents

- [Follow-up topics](CppFollowUpTopics.md) lists proposed up-to-C++20 collections and a separate C++23-delta curriculum.
- The [base generation prompt](CppProblemsGenerationPrompt.md) defines the exercise-pair format and general quality requirements.
- The [Level B interview-idiom plan](LevelBInterviewIdiomsPlan.md) defines the curriculum between atomic fluency exercises and full interview-problem practice.

## Validation

Validate the collections from this directory with:

```bash
tools/validate_exercises.sh collections/core c++20
tools/validate_exercises.sh collections/non_owning_views_and_ranges c++20
tools/validate_exercises.sh collections/ownership_move_semantics_and_raii c++20
tools/validate_exercises.sh collections/templates_and_concepts c++20
tools/validate_exercises.sh collections/text_processing_and_conversion c++20
tools/validate_exercises.sh collections/numeric_and_bit_manipulation c++20
tools/validate_exercises.sh collections/variants_and_error_modelling c++20
tools/validate_exercises.sh collections/custom_value_types_and_comparisons c++20
tools/validate_exercises.sh collections/callable_utilities c++20
tools/validate_exercises.sh collections/chrono c++20
tools/validate_exercises.sh collections/filesystem c++20
tools/validate_exercises.sh collections/cpp20_language_features c++20
tools/validate_exercises.sh collections/concurrency c++20
tools/validate_exercises.sh collections/compile_time_programming c++20
tools/validate_exercises.sh collections/stream_and_file_io c++20
tools/validate_exercises.sh collections/container_operations_and_iterator_mechanics c++20
tools/validate_exercises.sh collections/b_level/sequence_scanning_and_window_idioms c++20
../../.venv/bin/python tools/test_sequence_scanning_and_window_idioms.py
tools/validate_exercises.sh collections/b_level/linked_list_pointer_rewiring c++20
../../.venv/bin/python tools/test_linked_list_pointer_rewiring.py
tools/validate_exercises.sh collections/b_level/dynamic_programming_state_idioms c++20
../../.venv/bin/python tools/test_dynamic_programming_state_idioms.py
tools/validate_exercises.sh collections/b_level/monotonic_stack_and_deque_idioms c++20
../../.venv/bin/python tools/test_monotonic_stack_and_deque_idioms.py
tools/validate_exercises.sh collections/b_level/tree_traversal_and_recursive_state c++20
../../.venv/bin/python tools/test_tree_traversal_and_recursive_state.py
tools/validate_exercises.sh collections/b_level/graph_traversal_and_visitation c++20
../../.venv/bin/python tools/test_graph_traversal_and_visitation.py
tools/validate_exercises.sh collections/b_level/interval_merging_and_sweep_events c++20
../../.venv/bin/python tools/test_interval_merging_and_sweep_events.py
tools/validate_exercises.sh collections/b_level/heap_frontier_and_streaming_state c++20
../../.venv/bin/python tools/test_heap_frontier_and_streaming_state.py
tools/validate_exercises.sh collections/b_level/disjoint_set_connectivity_bookkeeping c++20
../../.venv/bin/python tools/test_disjoint_set_connectivity_bookkeeping.py
tools/validate_exercises.sh collections/b_level/backtracking_and_reversible_state c++20
../../.venv/bin/python tools/test_backtracking_and_reversible_state.py
tools/validate_exercises.sh collections/b_level/partition_and_selection_idioms c++20
../../.venv/bin/python tools/test_partition_and_selection_idioms.py
```

The validator compiles temporary completed forms through a pipe; it does not modify learner files or leave generated solutions in the repository.

## Adding a Collection

1. Create a Level A collection under `collections/<descriptive_name>/`, or a Level B interview-idiom collection under `collections/b_level/<descriptive_name>/`.
2. Write `collection_spec.md` before generating exercises.
3. Add `collection.json` with a stable, globally unique ID when progress should be portable or syncable.
4. Add `environment.json` when the evaluation harness should receive explicit target-language, library, or tool restrictions.
5. Create `exercise_manifest.md` and treat it as the collection inventory.
6. Add `exercise_order.md` when the collection has a canonical introduction order.
7. Generate and validate exercises in reviewable batches.
8. Reassess gaps after each batch and freeze the collection when only weak variants remain.
