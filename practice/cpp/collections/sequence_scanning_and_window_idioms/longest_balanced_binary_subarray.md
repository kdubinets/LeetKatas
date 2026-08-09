# Name

Longest Balanced Binary Subarray

# Description

Use first-occurrence prefix state to return the greatest length of a range in binary `values` containing equally many zeroes and ones. Treat zero and one as opposite balance changes, and retain only the earliest one-past prefix position for each balance so their distance is the matching range length.

# Solution

```cpp
std::unordered_map<int, std::size_t> first_position{{0, 0}};
int balance = 0;
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
