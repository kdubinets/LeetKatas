# Level B Interview-Idiom Collections

This namespace contains Level B C++ collections: short exercises in which the learner is given a named interview implementation idiom and its invariant, then implements its state transitions and control flow.

Level B is deliberately separate from Level A collections in the parent directory, which train atomic C++ implementation fluency, and from Level C problem practice, which requires algorithm selection and reasoning.

Each child directory is a complete collection with its own `collection_spec.md`, `exercise_manifest.md`, `collection.json`, `environment.json`, and (when a canonical introduction sequence is useful) `exercise_order.md`. Follow the Level B curriculum and authoring rules in [`../../LevelBInterviewIdiomsPlan.md`](../../LevelBInterviewIdiomsPlan.md).

## Available Collections

- [Sequence Scanning and Window Idioms](sequence_scanning_and_window_idioms/collection_spec.md): 19 supplied sequence-scanning, window, pointer, prefix-state, difference-array, and manual binary-search idioms.
- [Linked-List Pointer Rewiring](linked_list_pointer_rewiring/collection_spec.md): six supplied singly linked node-rewiring idioms with caller-owned nodes and constant auxiliary space; provisional and not corpus-audited.
- [Dynamic Programming State Idioms](dynamic_programming_state_idioms/collection_spec.md): ten supplied-recurrence exercises covering rolling storage, dependency order, sentinels, coupled states, predecessor aggregation, and memoization; provisional and not corpus-audited.
- [Monotonic Stack and Deque Idioms](monotonic_stack_and_deque_idioms/collection_spec.md): seven supplied ordered-candidate exercises covering stacks, deques, equality, expiration, and finalization; provisional and not corpus-audited.
- [Tree Traversal and Recursive State](tree_traversal_and_recursive_state/collection_spec.md): six supplied traversal exercises covering returned summaries, ancestor context, accumulators, and explicit suspension; provisional and not corpus-audited.
- [Graph Traversal and Visitation](graph_traversal_and_visitation/collection_spec.md): six supplied traversal exercises covering discovery, components, coloring, indegrees, multiple sources, and active state; provisional and not corpus-audited.
- [Interval Merging and Sweep Events](interval_merging_and_sweep_events/collection_spec.md): four supplied interval exercises covering active intervals, insertion phases, paired frontiers, and event ties; provisional and not corpus-audited.
- [Heap Frontier and Streaming State](heap_frontier_and_streaming_state/collection_spec.md): four supplied heap exercises covering merge frontiers, bounded candidates, stale distances, and balanced stream halves; provisional and not corpus-audited.
- [Disjoint-Set Connectivity Bookkeeping](disjoint_set_connectivity_bookkeeping/collection_spec.md): three supplied union-find exercises covering path shortening, weighted attachment, and component counts; provisional and not corpus-audited.
- [Backtracking and Reversible State](backtracking_and_reversible_state/collection_spec.md): six supplied search exercises covering path, marker, grid, duplicate, and coupled occupancy restoration; provisional and not corpus-audited.
- [Partition and Selection Idioms](partition_and_selection_idioms/collection_spec.md): two supplied exercises covering three-way regions and selection-range shrinking; provisional and not corpus-audited.
