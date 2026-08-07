# Name

Filter and Transform a View

# Description

Return `long long` squares of only the odd integers from a const vector, preserving order and leaving the input unchanged. This exercise covers composing lazy filtering and transformation before C++20 materialization.

# Solution

```cpp
auto squares = values |
               std::views::filter([](int value) { return value % 2 != 0; }) |
               std::views::transform([](int value) {
                   return static_cast<long long>(value) * value;
               });
std::ranges::copy(squares, std::back_inserter(result));
```
