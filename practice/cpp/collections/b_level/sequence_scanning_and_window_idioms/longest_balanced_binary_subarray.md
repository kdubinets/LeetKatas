# Name

Longest Balanced Binary Subarray

# Description

Return the length of the longest nonempty contiguous range in `values` containing equally many zeroes and ones, or zero if no such range exists. Every input value is zero or one; empty input produces zero. Preserve values, and assume every prefix balance fits in long long.

The supplied pattern is first-occurrence prefix state: zero and one contribute opposite balance changes, and the earliest position for each balance remains available to maximize the matching span.

This exercise covers retaining earliest prefix-balance positions to maximize an equal-zero-one span.

# Solution

```cpp
std::unordered_map<long long, std::size_t> first_position{{0, 0}};
long long balance = 0;
std::size_t best = 0;
for (std::size_t index = 0; index < values.size(); ++index) {
    balance += values[index] == 0 ? -1 : 1;
    const std::size_t position = index + 1;
    const auto [found, inserted] = first_position.emplace(balance, position);
    if (!inserted) {
        best = std::max(best, position - found->second);
    }
}
return best;
```
