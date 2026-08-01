# Name

Long Long Dot Product

# Description

Given two const integer vectors of equal length, return the sum of each pair of corresponding values multiplied together. Multiplication and accumulation must both use `long long`, and neither input may be modified. This exercise covers a typed inner product.

# Solution

```cpp
return std::inner_product(
    left.begin(), left.end(), right.begin(), 0LL, std::plus<>{},
    [](int a, int b) { return static_cast<long long>(a) * b; });
```
