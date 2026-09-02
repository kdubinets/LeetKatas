# Name

Manual First-Not-Less Binary Search

# Description

Use a half-open manual lower-bound loop to return the first index in ascending `values` whose value is not less than `target`. Return `values.size()` when every value is smaller. The candidate interval must retain the insertion position, not only existing values equal to the target.

# Solution

```cpp
std::size_t low = 0;
std::size_t high = values.size();
while (low < high) {
    const std::size_t middle = low + (high - low) / 2;
    if (values[middle] < target) {
        low = middle + 1;
    } else {
        high = middle;
    }
}
return low;
```
