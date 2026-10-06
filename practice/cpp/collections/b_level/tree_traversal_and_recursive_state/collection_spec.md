# Tree Traversal and Recursive State

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

Four initial exercises cover postorder failure state, returned-state plus aggregate state, ancestor context, and downward accumulation. Reassessment added explicit inorder suspension and postorder node propagation. Plain maximum depth was rejected as too small; path-vector restoration is reserved for the backtracking collection.

## Contract

All exercises use caller-owned, finite, acyclic binary trees. They do not allocate, delete, or mutate nodes. The traversal order, state meaning, base case, and propagation rule are supplied in Pattern. Learners implement one invariant in 3–8 minutes. Finish independently specifies observable behavior and constraints.

Each learner source supplies the node model and public entry function. Helpers, accumulators, bounds, and initialization belong to the learner implementation. Finish defines the complete observable task independently of the hint, including tree validity and mutation constraints.

## Included State Shapes

- Optional postorder height carrying either success or failure.
- Returned subtree height plus a shared diameter aggregate.
- Optional ancestor bounds propagated downward.
- A numeric prefix accumulated along root-to-leaf paths.
- An explicit stack that suspends and resumes inorder traversal.
- A postorder node result propagated from child subtrees.

## Exclusions

Generic recursive traversal, plain depth, tree construction, ownership, tree mutation, serialization, graph-like visited sets, and reversible shared path state are outside this collection.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/tree_traversal_and_recursive_state c++20
```

Runtime checks should use generated tree shapes and independent structural references, including empty, skewed, duplicate-valued, boundary-valued, balanced, and unbalanced trees.
