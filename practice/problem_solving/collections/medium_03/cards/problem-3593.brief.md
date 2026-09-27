# Minimum Increments to Equalize Leaf Paths

An undirected tree with `n` nodes is rooted at node 0. Node `i` has positive cost `cost[i]`; a root-to-leaf path’s score is the sum of its node costs, including both endpoints. You may increase any node by any nonnegative amount. Return the **fewest distinct nodes** whose cost must increase to make all root-to-leaf path scores equal.

`2 ≤ n ≤ 100,000`; costs are at most `10^9`. A tree with only one leaf needs zero changes.
