# Name

Find a Sorted Two-Sum Pair

# Description

Use converging two pointers to find two distinct values in ascending `values` whose sum equals `target`. Return their zero-based index pair, or an empty optional when none exists. The ordered input lets each comparison discard exactly one endpoint.

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
