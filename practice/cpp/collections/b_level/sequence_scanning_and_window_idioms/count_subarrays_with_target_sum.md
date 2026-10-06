# Name

Count Target-Sum Subarrays

# Description

Return the number of nonempty contiguous ranges in `values` whose elements sum to `target`. Overlapping ranges count separately, negative values are allowed, and empty input produces zero. Preserve values. All prefix sums and their differences from target fit in long long; the result fits in size_t.

The supplied pattern is a prefix-frequency scan initialized with one empty prefix of sum zero: prior prefix counts describe positions strictly before the current prefix, so a matching earlier prefix identifies a nonempty target-sum range.

This exercise covers counting target-sum subarrays by querying prior prefix frequencies before recording the current prefix.

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
