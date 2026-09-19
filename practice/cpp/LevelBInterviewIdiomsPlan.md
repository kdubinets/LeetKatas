# Level B C++ Interview Implementation Idioms

## Purpose

Level B is the bridge between Level A atomic C++ implementation fluency and full interview-problem practice. A Level B exercise gives the learner the algorithmic idiom to implement; the learner practises recalling and maintaining its standard state, invariant, and control flow.

It does not ask the learner to discover an algorithm, combine several independently selected patterns, or solve a complete LeetCode problem unaided.

## Exercise contract

- One named, reusable interview implementation idiom.
- One primary state-management or invariant-maintenance objective.
- Normally 3–8 minutes of learner-written code.
- Exactly one `// Finish:` section and the normal paired `.cpp` / `.md` format.
- The learner source explicitly names the pattern and its invariant, without revealing exact APIs or code.
- Metadata keeps `# Name`, `# Description`, and `# Solution`; its description names the pattern, invariant, inputs, constraints, and implementation skill.
- One canonical exercise per idiom by default. Add a variation only when it changes the state shape, invariant, or primary implementation decision.

Example source guidance:

```cpp
// Pattern: sliding window. Keep the current window valid by shrinking its left edge.
// Finish: return the greatest valid window length
```

## Development route

1. Create a Level B core collection from established, reusable idioms.
2. Extend the library through focused follow-up collections, each organized around one state-model family.
3. Mine solved medium and hard C++ interview solutions for recurring patterns and gaps, using a dedicated Level B audit workflow and cumulative evidence ledger.

Generate the core in small, reviewable batches. Validate it against real solutions before declaring it complete or frozen. The existing Level A audit is not the right tool: it deliberately excludes the larger idioms that Level B is intended to cover.

## Initial core proposal

Start with `collections/b_level/sequence_scanning_and_window_idioms/`, targeting roughly 16–24 exercises. Its scope is sequential stateful scans, not every interview pattern.

Strong candidate families:

- fixed-size rolling windows;
- shrink-to-valid sliding windows with an explicit invariant;
- two pointers that converge or move in lockstep;
- slow/fast pointers for in-place sequence compaction;
- frequency-table maintenance during a scan;
- prefix sums and prefix-frequency state;
- difference-array range updates;
- manual binary-search loop variants.

Keep monotonic stacks and deques as candidates for a focused follow-up collection: their ordered unresolved state differs from the current scan and window invariants. Audit corpus evidence before extending the initial core or creating that follow-up.

## Roadmap after the initial core

### General-considerations follow-up

At the user's request, [Linked-List Pointer Rewiring](collections/b_level/linked_list_pointer_rewiring/collection_spec.md) was developed without parsing the LeetCode corpus. Its six exercises isolate whole-chain reversal, predecessor-based filtering, tail merging, two-chain stable partitioning, pair-block rewiring, and segment-boundary reconnection. It is an active provisional collection, not evidence that these are the most prevalent gaps or that linked-list coverage is complete. Other follow-ups and extension decisions retain the evidence-gathering route below.

At the user's request, [Dynamic Programming State Idioms](collections/b_level/dynamic_programming_state_idioms/collection_spec.md) was likewise developed without corpus extraction. Its ten exercises supply their recurrences and isolate rolling scalar state, rolling rows, zero-one and reusable-choice update direction, preservation of overwritten dependencies, explicit unreachable and uncomputed states, coupled state snapshots, and predecessor aggregation. It remains provisional and makes no corpus-coverage claim.

[Monotonic Stack and Deque Idioms](collections/b_level/monotonic_stack_and_deque_idioms/collection_spec.md) now supplies seven general-considerations exercises. Five initial candidates cover unresolved indices, strict boundaries, spans, expiration, and histogram finalization; reassessment retained bounded greedy popping and two-ended prefix-candidate maintenance as distinct invariants. It remains provisional and makes no corpus-coverage claim.

[Tree Traversal and Recursive State](collections/b_level/tree_traversal_and_recursive_state/collection_spec.md) supplies six general-considerations exercises. Four initial candidates cover postorder failure, returned and aggregate state, ancestor bounds, and path accumulation; reassessment retained explicit inorder suspension and lowest-common-ancestor node propagation. Plain depth and shared-path restoration were rejected as weak or better owned elsewhere. It remains provisional and makes no corpus-coverage claim.

[Graph Traversal and Visitation](collections/b_level/graph_traversal_and_visitation/collection_spec.md) supplies six general-considerations exercises. Five initial candidates cover enqueue-time discovery, component starts, coloring, indegree transitions, and multi-source initialization; reassessment retained active-versus-complete directed cycle state. Weighted frontiers remain separate. It remains provisional and makes no corpus-coverage claim.

[Interval Merging and Sweep Events](collections/b_level/interval_merging_and_sweep_events/collection_spec.md) and [Heap Frontier and Streaming State](collections/b_level/heap_frontier_and_streaming_state/collection_spec.md) implement the roadmap's scope split. Each has four general-considerations exercises. Reassessment deliberately added no padding: interval union-length and maximum-overlap variants duplicate existing state, while heap-based rooms and kth variants duplicate the interval and bounded-retention exercises. Both remain provisional and make no corpus-coverage claim.

[Disjoint-Set Connectivity Bookkeeping](collections/b_level/disjoint_set_connectivity_bookkeeping/collection_spec.md) is intentionally a compact three-exercise module covering path halving, weighted attachment, and component-count updates after successful unions. Reassessment rejected rank/path-compression symmetry and larger connectivity stories. It remains provisional and makes no corpus-coverage claim.

[Backtracking and Reversible State](collections/b_level/backtracking_and_reversible_state/collection_spec.md) supplies six general-considerations exercises. Four initial candidates cover shared paths, used markers, reusable choices, and temporary grid state; reassessment retained same-depth duplicate suppression and coupled queen occupancy. [Partition and Selection Idioms](collections/b_level/partition_and_selection_idioms/collection_spec.md) is intentionally a two-exercise module matching the roadmap's two distinct invariants. Both remain provisional and make no corpus-coverage claim.

The general-considerations pass reassessed both candidates that previously required stronger evidence and did not create collections for them. Structured parsing produced either atomic bracket-stack mechanics or tasks dominated by grammar/tokenization and full parser design. Coupled representations produced either atomic container operations or multi-operation data-structure implementations with excessive supplied machinery. Keep both as corpus-audit candidates; add them only when recurring solutions expose a bounded 3–8 minute invariant not already trained elsewhere.

The general-considerations pass is complete with 54 exercises across ten follow-up collections, in addition to the 19-exercise sequence-scanning collection. Every built family has an initial set, a recorded reassessment, compilation validation, and targeted runtime checks. All collections remain provisional pending corpus evidence; completion of this pass is not a claim that the Level B curriculum is frozen.

Create a collection only when enough non-duplicate exercises share its state model. The examples below are candidates for evidence gathering, not approved exercise inventories. Supply the applicable algorithm and isolate one implementation invariant in each exercise.

### Established areas and scope decisions

| Area | Assessment and candidate implementation skills | Scope boundary |
|---|---|---|
| Monotonic stacks and deques | Built provisionally with unresolved indices, strict boundaries, spans, expiration, finalization, bounded popping, and prefix candidates. | "Ordered-boundary searches" means boundaries maintained by a stack or deque here. Do not repeat ordinary lower/upper-bound loops already covered by the initial core. Supply the ordering and equality rules. |
| Trees and recursive state propagation | Built provisionally with postorder summaries, ancestor bounds, downward accumulation, explicit inorder suspension, and node-result propagation. | Avoid vague "implement DFS" tasks. Supply the traversal and state meaning; do not ask the learner to discover the recurrence or combine independently chosen patterns. Keep reversible constructed-search state in backtracking. |
| Graph traversal state and visitation discipline | Built provisionally with enqueue-time marking, components, coloring, multi-source initialization, indegrees, and three-state cycle detection. | Supply the graph representation and traversal rules. Each exercise needs a distinct state decision; changing only the graph's story or storage format does not justify another exercise. |
| Linked-list pointer rewiring | Built provisionally with reversal, predecessor removal, tail merging, stable partitioning, pair blocks, and segment reconnection. | Supply the node model, ownership rules, and applicable pointer strategy. Focus on link invariants rather than memory-management design or a complete linked-list implementation. |
| Intervals, heaps, and event scheduling | Built provisionally as separate interval/sweep and heap-frontier collections because their state models differ. | Place event exercises with the family whose invariant they train. Supply sorting and tie rules; do not duplicate meeting concurrency across both families. |
| Disjoint sets and connectivity bookkeeping | Built provisionally as a compact module covering path halving, union by size, and successful-union component counts. | Supply the parent/size representation and supporting operations needed to isolate the task. Do not ask for an entire DSU implementation or pad the module to match larger collections. |

### Additional established areas

| Area | Candidate implementation skills | Scope boundary |
|---|---|---|
| Backtracking and reversible state | Built provisionally with path, marker, grid, duplicate-suppression, and coupled-occupancy restoration. | Supply choices, stopping conditions, and pruning. This area constructs branches, whereas tree traversal visits an existing structure. |
| Dynamic-programming implementation with a supplied recurrence | Built provisionally with rolling storage, update order, sentinels, memoization, coupled states, predecessor aggregation, and row rotation. | Supply state meaning, recurrence, base cases, and dependency order. Train implementation rather than recurrence discovery or optimization selection. |
| Partition-based selection | Built provisionally as a compact module with three-way regions and quickselect range shrinking. | Supply the pivot strategy and region invariant. For selection, provide the partition helper so the learner implements one range-maintenance idiom rather than combining two algorithms. |

Backtracking is the strongest addition to the original roadmap because its choice/recurse/undo discipline is broadly reusable and differs from the current collection's sequential state.

### Candidates requiring stronger evidence

- Structured parsing with context stacks: maintain nested frames or operator state with tokenization and grammar supplied. Keep tasks bounded; a complete or long parser is outside this format.
- Maintaining coupled representations: implement one operation that preserves a shared invariant, such as updating a supplied LRU cache's list and key-to-iterator map. Supply the data model and supporting machinery rather than asking for a complete data structure. Confirm that the operation offers a meaningful 3–8 minute Level B objective rather than a short Level A API task.

Treat grids, multi-source BFS, monotonic deques, and cycle detection as possible extensions of traversal, monotonic-structure, or pointer families. A new setting or variant does not automatically warrant another collection.

The coroutine direction in `CppFollowUpTopics.md` belongs to a separate advanced C++ curriculum with its own exercise contract. Its supporting machinery and library-development focus make it a weaker fit for this interview-idiom roadmap; do not include it merely because an exercise takes longer than Level A's one-minute target.

### Prioritization and evidence

Begin corpus evidence gathering with monotonic structures, tree state, graph visitation, linked-list rewiring, backtracking, supplied-recurrence DP, and partition/selection. Use evidence to retain, amend, extend, merge, or remove provisional exercises rather than assuming the general-considerations inventory is final.

Compare candidates against all existing Level B manifests and the Level A core. Build the family with the strongest recurring, distinct gaps, allowing evidence to change the provisional order. Audit the existing 19-exercise collection before deciding which exercises to retain, amend, or extend.

This is a roadmap, not a quota. Do not assign a predetermined exercise count to every area or assume that each area needs its own collection. Leave a family unbuilt if it produces only weak variants or belongs more naturally in normal problem practice.

## Application integration

The existing Neovim driver can launch and schedule a Level B collection without UI changes. Give each collection a stable `collection.json`, C++20 `environment.json`, manifest, and canonical `exercise_order.md`.

Begin with the current compile-and-review workflow. Add deterministic runtime test support later when several Level B exercises demonstrate a clear need for it; it is a reliability enhancement, not a prerequisite or a replacement for reviewer feedback.

## Evidence and tools

Use `$develop-cpp-level-b-idioms` for planning, creating, or reviewing Level B collections. Use GPT-5.6 Terra with high reasoning effort as the default; reserve Sol for difficult boundary judgments or final audits.

After the initial core exists, add a separate Level B audit skill. It should use seeded, stratified, unseen-first samples of solved C++ medium and hard solutions, a hash-aware ledger distinct from the Level A ledger, and explicit classifications for trained idioms, partial coverage, candidate gaps, duplicate variations, and out-of-scope algorithm discovery.
