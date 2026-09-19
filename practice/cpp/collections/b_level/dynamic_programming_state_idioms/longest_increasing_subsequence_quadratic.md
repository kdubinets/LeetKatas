# Name

Longest Increasing Subsequence by Predecessors

# Description

Return the greatest length of a strictly increasing subsequence in index order; indices need not be contiguous and equal values do not extend it. Empty input returns zero. Do not modify values.

The supplied state for each index starts at one and aggregates every earlier state whose value is smaller.

This exercise covers aggregation over a variable set of valid predecessor states.

# Solution

```cpp
if (values.empty()) {
    return 0;
}
std::vector<std::size_t> lengths(values.size(), 1);
std::size_t answer = 1;
for (std::size_t current = 0; current < values.size(); ++current) {
    for (std::size_t previous = 0; previous < current; ++previous) {
        if (values[previous] < values[current]) {
            lengths[current] = std::max(lengths[current], lengths[previous] + 1);
        }
    }
    answer = std::max(answer, lengths[current]);
}
return answer;
```
