# Name

Count Target-Sum Subarrays

# Description

Use a prefix-frequency scan to count contiguous subarrays of `values` whose sum equals `target`, including negative values. Before recording each current prefix sum, count how often the prefix `current - target` has already occurred; this order preserves subarray direction.

# Solution

```cpp
std::unordered_map<long long, std::size_t> frequencies{{0, 1}};
long long prefix = 0;
std::size_t result = 0;
for (int value : values) {
    prefix += value;
    if (const auto found = frequencies.find(prefix - target); found != frequencies.end()) {
        result += found->second;
    }
    ++frequencies[prefix];
}
return result;
```
