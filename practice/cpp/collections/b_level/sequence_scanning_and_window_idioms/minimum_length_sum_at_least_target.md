# Name

Minimum Sufficient Sum Window

# Description

Return the length of the shortest nonempty contiguous range in `positive_values` whose elements sum to at least `target`, or zero if no such range exists. Every input value and the target are strictly positive. Empty input produces zero.

The supplied pattern is a shrinking positive-sum sliding window: advancing its left boundary decreases the sum, allowing sufficient windows to be shortened.

This exercise covers minimizing a sufficient positive-sum window by advancing its left boundary while it meets the target.

# Solution

```cpp
std::size_t left = 0;
std::size_t best = positive_values.size() + 1;
long long sum = 0;
for (std::size_t right = 0; right < positive_values.size(); ++right) {
    sum += positive_values[right];
    while (sum >= target) {
        best = std::min(best, right - left + 1);
        sum -= positive_values[left];
        ++left;
    }
}
return best == positive_values.size() + 1 ? 0 : best;
```
