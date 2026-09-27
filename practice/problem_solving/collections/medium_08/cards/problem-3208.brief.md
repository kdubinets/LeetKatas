# Alternating Groups II

Binary colors form a circle of n tiles. Count the n possible starting positions whose next k tiles, read in circular order, alternate: every adjacent pair **inside that length-k sequence** must have different colors. A group does not additionally compare its last tile with its first, even when k=n.

`3 <= n <= 100000`, `colors[i]` is 0 or 1, and `3 <= k <= n`. Distinct starting positions count separately.
