# Name

Count All-Distinct Fixed Windows

# Description

Return the number of contiguous groups of exactly `width` elements in `values` containing no repeated value. Overlapping groups count separately. Return zero when `width` is zero or exceeds `values.size()`. Preserve values.

The supplied pattern is a fixed-size frequency window whose counts represent exactly the current group of elements.

This exercise covers maintaining fixed-window frequency state while counting windows with distinct values.

# Solution

```cpp
if (width == 0 || width > values.size()) {
    return 0;
}

std::unordered_map<int, std::size_t> counts;
std::size_t result = 0;
for (std::size_t right = 0; right < values.size(); ++right) {
    ++counts[values[right]];
    if (right >= width) {
        const int leaving = values[right - width];
        if (--counts[leaving] == 0) {
            counts.erase(leaving);
        }
    }
    if (right + 1 >= width && counts.size() == width) {
        ++result;
    }
}
return result;
```
