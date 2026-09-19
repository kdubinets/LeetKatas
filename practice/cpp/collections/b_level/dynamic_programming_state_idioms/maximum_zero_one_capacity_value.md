# Name

Maximum Zero-One Capacity Value

# Description

Return the greatest total value of a subset whose total weight is at most capacity. The weight and value vectors have equal length, every weight is positive, every value is nonnegative, and each item may be selected at most once. Empty input and zero capacity produce zero. Do not modify either input. All values and sums fit in long long.

The supplied zero-one dynamic-programming transition uses one capacity row. Capacities are visited from high to low for each item so a transition reads the state that existed before processing that item.

This exercise covers descending in-place capacity updates for zero-one choices.

# Solution

```cpp
std::vector<long long> best(capacity + 1, 0);
for (std::size_t item = 0; item < weights.size(); ++item) {
    const std::size_t weight = weights[item];
    if (weight > capacity) {
        continue;
    }
    for (std::size_t current = capacity; current >= weight; --current) {
        best[current] = std::max(
            best[current],
            best[current - weight] + static_cast<long long>(values[item]));
        if (current == weight) {
            break;
        }
    }
}
return best[capacity];
```
