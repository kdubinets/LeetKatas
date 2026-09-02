# Name

Count All-Distinct Fixed Windows

# Description

Use a fixed-size frequency window to count contiguous windows of `width` integers that contain no repeated value. Return zero when `width` is zero or exceeds `values.size()`. The invariant is that the frequency state represents exactly the current window.

# Solution

```cpp
std::unordered_map<int, int> counts;
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
