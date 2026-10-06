# Name

Maximum Fixed-Window Sum

# Description

Return the greatest sum among all contiguous groups of exactly `width` elements in `values`. The greatest sum may be negative. Preserve values, and assume all intermediate sums fit in long long. Return zero when `width` is zero or exceeds the input size.

The supplied pattern is a fixed-size rolling window whose running total equals the sum of the current group.

This exercise covers maintaining a rolling numeric total for a fixed-width window.

# Solution

```cpp
if (width == 0 || width > values.size()) {
    return 0;
}

long long current = 0;
for (std::size_t index = 0; index < width; ++index) {
    current += values[index];
}

long long best = current;
for (std::size_t right = width; right < values.size(); ++right) {
    current += values[right];
    current -= values[right - width];
    best = std::max(best, current);
}
return best;
```
