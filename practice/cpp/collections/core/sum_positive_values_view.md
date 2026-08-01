# Name

Sum Positive Values Through a View

# Description

Return the `long long` sum of only the positive integers in a const vector, leaving the input unchanged. This exercise covers lazily filtering a C++20 range before numeric accumulation.

# Solution

```cpp
auto positive_values =
    values | std::views::filter([](int value) { return value > 0; });
return std::accumulate(positive_values.begin(), positive_values.end(), 0LL);
```
