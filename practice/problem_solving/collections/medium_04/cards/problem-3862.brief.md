# Find the Smallest Balanced Index

For an array of **positive** integers, index `i` is balanced when the sum of elements strictly before it equals the product of elements strictly after it. An empty left side has sum 0; an empty right side has product 1. Return the smallest balanced index, or `-1` if none exists. The array has at most 100,000 entries, each at most 10^9.

In `[2,8,2,2,5]`, index 2 is balanced: the left sum is 10 and the right product is 10.
