# Name

Maximum Fixed-Window Sum

# Description

Use the fixed-size rolling-window pattern to return the greatest sum of any contiguous `width` values in `values`. `width` may be zero or exceed the input size, in which case return zero. Maintain the current window total as values enter and leave instead of recomputing each window.

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
