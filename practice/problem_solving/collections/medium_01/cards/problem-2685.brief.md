# Count the Number of Complete Components

An undirected graph has `n` vertices numbered `0` through `n - 1` and a list
of edges. Count its connected components in which every pair of distinct
vertices has an edge between them. An isolated vertex counts as a complete
component.

For example, with `n = 4` and edges `[[0,1],[1,2]]`, the only complete
component is the isolated vertex `3`, so the answer is `1`.

`1 ≤ n ≤ 50`. Edges have distinct endpoints, and no edge is repeated.
