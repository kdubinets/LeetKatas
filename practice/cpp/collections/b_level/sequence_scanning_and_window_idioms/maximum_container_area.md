# Name

Maximum Two-Endpoint Container Area

# Description

Return the maximum area among pairs of indices `i < j` in nonnegative `heights`. The area is `(j - i)` times the smaller of `heights[i]` and `heights[j]`. Return zero when fewer than two elements exist. Preserve heights, and assume every area fits in long long.

The supplied pattern is converging two pointers: after a pair is measured, its smaller-height endpoint is dominated; either endpoint may be discarded when heights are equal.

This exercise covers discarding the dominated endpoint while measuring converging two-pointer container pairs.

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
