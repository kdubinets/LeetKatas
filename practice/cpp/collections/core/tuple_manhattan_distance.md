# Name

Tuple Manhattan Distance

# Description

Read three integer coordinates from a const `std::tuple<int, int, int>` and return the `long long` sum of their absolute values. Each absolute value and the total must use `long long` arithmetic so every `int` coordinate is handled safely. This exercise covers unpacking a tuple with structured bindings.

# Solution

```cpp
const auto& [x, y, z] = point;
return std::abs(static_cast<long long>(x)) +
       std::abs(static_cast<long long>(y)) +
       std::abs(static_cast<long long>(z));
```
