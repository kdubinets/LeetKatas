# Stone Game II

Positive stone piles are arranged in a row. Two players alternate, starting with Alice. On a turn, take all stones in the first `X` remaining piles, where `1 <= X <= 2M` and there must be at least `X` piles remaining. Then set `M` to `max(M, X)`. Initially `M=1`. Play ends when all piles have been taken. Both players maximize their own stone total. Return the number of stones Alice can secure under optimal play.

`1 <= piles.length <= 100` and `1 <= piles[i] <= 10000`.
