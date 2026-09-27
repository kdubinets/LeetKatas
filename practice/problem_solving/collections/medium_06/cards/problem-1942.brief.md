# The Number of the Smallest Unoccupied Chair

Friends `0` through `n-1` each have an arrival and leaving time. Arrival times are distinct. On arrival a friend takes the smallest-numbered currently unoccupied chair from an unbounded sequence `0,1,2,...`. A departure frees its chair **at** its leaving time, so a friend arriving then may use it. Return the chair assigned to `targetFriend`.

`2 <= n <= 10000`; `1 <= arrival < leaving <= 100000`; `0 <= targetFriend < n`.
