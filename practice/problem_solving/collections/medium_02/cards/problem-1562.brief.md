# Find Latest Group of Size M

Start with a binary string of `n` zeros. The array `arr` is a permutation of
positions `1` through `n`; at step `i`, set position `arr[i]` to `1` (using
1-based positions and steps). A group of ones is a **maximal** contiguous run:
it cannot be extended left or right by another `1`.

For `arr = [1,3,2]` and `m = 1`, the answer is step `2`; after step `3`,
the single run has length `3`.

Return the latest step at which some group has length **exactly** `m`, or
`-1` if no such step exists. `1 ≤ m ≤ n ≤ 10^5`.
