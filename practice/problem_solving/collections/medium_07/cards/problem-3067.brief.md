# Count Pairs of Connectable Servers in a Weighted Tree Network

Given a weighted undirected tree with servers `0` through `n-1` and a positive `signalSpeed`, return one count for each server `c`. Count unordered pairs of distinct servers `a,b`, both different from `c`, such that each path distance from `c` to its endpoint is divisible by `signalSpeed`, and the two paths share no edge. Path distance is the sum of its edge weights.

`2 <= n <= 1000`; there are `n-1` edges; weights and `signalSpeed` are in `[1,10^6]`.
