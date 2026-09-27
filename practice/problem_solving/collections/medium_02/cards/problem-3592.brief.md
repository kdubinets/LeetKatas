# Inverse Coin Change

You are given an array of `n` counts in amount order: the first entry is the
number of ways to pay amount `1`, the second is for amount `2`, and the nth
is for amount `n`. Each way is a **combination** of coins; using the same
denominations in a different order does not make a new way. The denominations
have been lost. Each is a distinct positive integer at most `n`, and each
may be used any number of
times. Recover the sorted set of denominations that yields **all** the given
counts, or return an empty array if none does. The empty set is also a valid
answer when every given count is zero.

For counts `[1,2]`, denominations `[1,2]` work: amount `1` has `[1]`, and
amount `2` has `[1,1]` and `[2]`.

`1 ≤ n ≤ 100`, and each count is between `0` and `2 × 10^8`.
