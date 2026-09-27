# Minimize the Maximum Difference of Pairs

Choose `p` pairs of **distinct indices** from an integer array, with no index used in more than one pair. Minimize the largest absolute difference within any selected pair and return that value. When `p=0`, the answer is defined as 0. The array has up to 100,000 values in `[0,10^9]`; `p` is at most half its length.

For `[10,1,2,7,1,3]` and `p=2`, pairs of values `(1,1)` and `(2,3)` achieve a largest difference of 1.
