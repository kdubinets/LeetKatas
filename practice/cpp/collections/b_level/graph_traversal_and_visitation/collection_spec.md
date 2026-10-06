# Graph Traversal and Visitation

## Status

Active provisional Level B collection designed from general considerations without corpus extraction. It is not complete, corpus-audited, or frozen.

Five initial exercises cover enqueue-time discovery, component starts, two-color state, indegree transitions, and multi-source initialization. Reassessment retained directed cycle colors because active-versus-complete visitation is a distinct state model. Story-only BFS/DFS variants and separate cycle stories were rejected.

## Contract

Adjacency lists use zero-based vertex identifiers and valid endpoints. The representation, traversal, marking time, state meaning, and neighbor rules are supplied. Learners implement one visitation invariant in 3–8 minutes rather than select an algorithm.

Each learner source supplies only the public entry function, a pattern hint, and one Finish comment describing the complete task, including relevant edge cases. State storage, initialization, traversal, and any recursive helper belong to the learner's implementation. Metadata restates the source contract and records a solution for the complete entry function.

## Included State Shapes

- Optional unweighted distances assigned at enqueue time.
- Component roots selected from still-unvisited vertices.
- Uncolored/two-color state with edge conflict detection.
- Indegree decrements whose transition to zero enqueues once.
- Simultaneous distance-zero initialization for many grid sources.
- Unvisited, active, and complete states for recursive directed traversal.

## Exclusions

Weighted frontier search belongs to the heap-frontier collection. Tree traversal without visited state, graph representation design, path reconstruction, strongly connected components, and algorithms requiring multiple independently selected phases are excluded.

## Verification

```bash
tools/validate_exercises.sh collections/b_level/graph_traversal_and_visitation c++20
```

Runtime checks should compare small generated graphs and grids with independent reachability, distance, coloring, ordering, and cycle references.
