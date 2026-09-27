# Apply Operations to Make All Array Elements Equal to Zero

Given a nonnegative-integer array `nums` and a positive integer `k`, you may
repeatedly choose any contiguous block of exactly `k` elements and decrease
each of those elements by one. Return whether some sequence of these
operations makes every element zero.

For example, `[1,1]` with `k = 2` is possible, while `[1,0,1]` with
`k = 2` is not.

`1 ≤ k ≤ nums.length ≤ 10^5`, and each original element is at most `10^6`.
