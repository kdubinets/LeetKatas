# Name

Sum Squared Values

# Description

Square each `int` in a const vector using widened arithmetic and return their `long long` sum. Empty input produces zero, and the caller guarantees the total fits. This exercise covers combining unary transformation and reduction in one standard numeric operation.

# Solution

```cpp
return std::transform_reduce(
    values.begin(), values.end(), 0LL, std::plus<>{},
    [](int value) { return 1LL * value * value; });
```
