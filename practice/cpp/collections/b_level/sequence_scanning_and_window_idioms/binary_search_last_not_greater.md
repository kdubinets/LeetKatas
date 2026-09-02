# Name

Manual Last-Not-Greater Binary Search

# Description

Use a half-open manual upper-bound loop to find the last index in ascending `values` whose value is not greater than `target`. Return no result if every value is greater. First locate the one-past-last acceptable position, then handle the empty-prefix case before converting it to the returned index.

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
