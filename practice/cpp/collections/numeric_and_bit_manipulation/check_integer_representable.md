# Name

Check Integer Representability

# Description

Return whether a `long long` value can be represented exactly by `int`, without first performing a potentially narrowing conversion or manually spelling the destination limits. This exercise covers the C++20 integral representability utility.

# Solution

```cpp
return std::in_range<int>(value);
```
