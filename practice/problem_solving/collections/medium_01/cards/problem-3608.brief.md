# Minimum Time for K Connected Components

An undirected graph has `n` numbered vertices. Each edge has a positive
integer removal time. At time `t`, all edges with removal time at most `t`
have been removed. Find the smallest nonnegative integer `t` at which the
remaining graph has at least `k` connected components. The graph may already
be disconnected at time `0`; isolated vertices count as components.

For example, with `n = 3`, one edge `[0,2,5]`, and `k = 2`, the answer is
`0`: vertex `1` is already separate.

`1 ≤ n ≤ 10^5`, `0 ≤ edges.length ≤ 10^5`, `1 ≤ k ≤ n`, and removal times are
at most `10^9`. Each edge joins two distinct vertices; no edge is repeated.
