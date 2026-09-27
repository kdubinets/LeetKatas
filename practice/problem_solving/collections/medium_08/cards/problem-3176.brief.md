# Find the Maximum Length of a Good Subsequence I

A subsequence is formed by deleting any number of elements while preserving the order of those kept. Its **change count** is the number of adjacent pairs in that subsequence having unequal values. Return the longest subsequence of `nums` with change count at most k.

For example, in `[1,2,1]` the whole sequence has two changes, so with `k=1` the maximum length is 2.

`1 <= n <= 500`, `1 <= nums[i] <= 10^9`, and `0 <= k <= min(n,25)`.
