# Name

Reduce an Integer Product

# Description

Return the product of a const vector of `int` values as a `long long`, using one as the result for an empty input. The caller guarantees that the product of all nonzero input values fits in `long long`, so every regrouped multiplication is representable. This exercise covers `std::reduce` with an explicitly widened identity and multiplication operation.

# Solution

```cpp
return std::reduce(
    values.begin(), values.end(), 1LL, std::multiplies<long long>{});
```
