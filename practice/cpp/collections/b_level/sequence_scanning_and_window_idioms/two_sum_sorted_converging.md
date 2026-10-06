# Name

Find a Sorted Two-Sum Pair

# Description

Return any pair of distinct zero-based indices whose values sum to `target`, or an empty optional if no such pair exists. The input is sorted in nondecreasing order and may contain duplicates, so the two selected values may be equal. Fewer than two elements cannot form a pair. Preserve values.

The supplied pattern is converging two pointers on sorted input, with each sum comparison determining which endpoint can be discarded.

This exercise covers moving converging sorted-sequence pointers according to the pair-sum comparison.

# Solution

```cpp
if (values.size() < 2) {
    return std::nullopt;
}

std::size_t left = 0;
std::size_t right = values.size() - 1;
while (left < right) {
    const long long sum = static_cast<long long>(values[left]) + values[right];
    if (sum == target) {
        return std::pair{left, right};
    }
    if (sum < target) {
        ++left;
    } else {
        --right;
    }
}
return std::nullopt;
```
