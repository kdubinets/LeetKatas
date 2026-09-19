# Name

Manual Last-Not-Greater Binary Search

# Description

Return the last zero-based index where `values[i] <= target`, or an empty optional if no such index exists, including for empty input. The input is sorted in nondecreasing order.

The supplied pattern is manual upper-bound search: the half-open search locates the one-past-last acceptable position before that boundary is converted to an index.

This exercise covers finding an upper boundary with manual binary search and safely converting it to the last acceptable index.

# Solution

```cpp
std::size_t low = 0;
std::size_t high = values.size();
while (low < high) {
    const std::size_t middle = low + (high - low) / 2;
    if (values[middle] <= target) {
        low = middle + 1;
    } else {
        high = middle;
    }
}
if (low == 0) {
    return std::nullopt;
}
return low - 1;
```
