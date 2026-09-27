# Construct the Minimum Bitwise Array II

For each prime integer `x` in an array, find the **smallest nonnegative** integer `v` such that `v OR (v+1) = x`, where OR is bitwise. Write `-1` if no such value exists. Return one answer per input in the same order. There are at most 100 inputs, each between 2 and 10^9.

For `x=7`, `v=3` works because `3 OR 4 = 7`, and it is the smallest such value; for `x=2`, no value works.
