# Name

Maximum Two-Endpoint Container Area

# Description

Use converging two pointers to return the greatest area formed by two distinct nonnegative `heights` positions. The area uses their distance and the smaller endpoint height. When fewer than two positions exist, return zero; after measuring a pair, move only the limiting endpoint.

# Solution

```cpp
if (heights.size() < 2) {
    return 0;
}

std::size_t left = 0;
std::size_t right = heights.size() - 1;
long long best = 0;
while (left < right) {
    const long long height = std::min(heights[left], heights[right]);
    best = std::max(best, height * static_cast<long long>(right - left));
    if (heights[left] < heights[right]) {
        ++left;
    } else {
        --right;
    }
}
return best;
```
