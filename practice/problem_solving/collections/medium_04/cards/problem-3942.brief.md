# Minimum Operations to Sort a Permutation

A permutation of `0` through `n-1` can be changed by either reversing the **whole** array or rotating it one position left (moving the first element to the end). Each use costs one operation. Return the fewest operations needed to reach increasing order, or `-1` if impossible. The array can have up to 100,000 elements.

For `[0,2,1]`, rotate left once and then reverse to obtain `[0,1,2]`, so the answer is 2.
