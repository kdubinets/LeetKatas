# Find X Value of Array I

Given a positive-integer array `nums` and an integer `k`, choose a prefix and
a suffix to remove. Either may be empty, they cannot overlap, and at least one
element must remain. Each choice of how many elements to remove from the two
ends is a distinct operation. For every remainder `x` from `0` through
`k - 1`, count the operations for which the product of the remaining elements
has remainder `x` modulo `k`.

Return these `k` counts in remainder order. The array has between 1 and
`10^5` elements, each between 1 and `10^9`; `1 ≤ k ≤ 5`.
A count may exceed the 32-bit signed integer range.
