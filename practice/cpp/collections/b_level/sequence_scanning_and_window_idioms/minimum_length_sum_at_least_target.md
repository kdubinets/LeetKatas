# Name

Minimum Sufficient Sum Window

# Description

Use a shrink-to-valid sliding window to return the smallest nonempty contiguous range of positive `positive_values` whose sum is at least positive `target`, or zero when no such range exists. Positivity makes removing the left value the correct way to minimize a currently sufficient window.

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
