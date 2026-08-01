# Name

Add Vectors Elementwise

# Description

Given two const integer vectors of equal length, return a `std::vector<long long>` containing the sum of each corresponding pair. Addition must use `long long`, and neither input may be modified. This exercise covers transforming two input ranges into one output range.

# Solution

```cpp
std::ranges::transform(left, right, result.begin(),
                       [](int a, int b) {
                           return static_cast<long long>(a) + b;
                       });
```
