# Name

Manual Exact Binary Search

# Description

Use a half-open manual binary-search loop to find `target` in ascending `values`. Return its index in an optional or no result when it is absent. The candidate interval `[low, high)` must contain every still-possible matching index and must shrink on every iteration.

# Solution

```cpp
std::size_t low = 0;
std::size_t high = values.size();
while (low < high) {
    const std::size_t middle = low + (high - low) / 2;
    if (values[middle] < target) {
        low = middle + 1;
    } else if (target < values[middle]) {
        high = middle;
    } else {
        return middle;
    }
}
return std::nullopt;
```
