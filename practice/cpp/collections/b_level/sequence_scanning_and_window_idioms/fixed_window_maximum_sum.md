# Name

Maximum Fixed-Window Sum

# Description

Return the greatest sum among all contiguous groups of exactly `width` elements in `values`. The greatest sum may be negative. The supplied guard returns zero when `width` is zero or exceeds the input size.

The supplied pattern is a fixed-size rolling window whose running total equals the sum of the current group.

This exercise covers maintaining a rolling numeric total for a fixed-width window.

# Solution

```cpp
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
