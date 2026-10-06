# Name

Manual Exact Binary Search

# Description

Return any zero-based index where `values` equals `target`, or an empty optional if no such index exists. The input is sorted in nondecreasing order, so duplicates are permitted. Empty input has no matching index. Preserve values.

The supplied pattern is manual binary search with a half-open candidate interval `[low, high)` containing every still-possible matching index.

This exercise covers maintaining a half-open candidate interval for exact manual binary search.

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
