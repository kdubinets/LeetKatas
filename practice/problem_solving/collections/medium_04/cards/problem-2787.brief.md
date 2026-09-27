# Ways to Express an Integer as Sum of Powers

Given positive integers `n` and `x`, count the **sets** of distinct positive integers whose xth powers sum exactly to `n`. Different orders of the same set count once, and each base may appear at most once. Return the count modulo 10^9+7. `n` is at most 300 and `x` is between 1 and 5.

For `n=10`, `x=2`, the only set is `{1,3}` because `1²+3²=10`, so the answer is 1.
