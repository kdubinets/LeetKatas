# Name

Equal Value Range Indices

# Description

Given a const ascending integer vector, return a pair of `std::size_t` indices delimiting the half-open range of all target occurrences. For an absent target, both indices must be its insertion position. This exercise covers finding both binary-search boundaries in one operation.

# Solution

```cpp
auto matches = std::ranges::equal_range(sorted_values, target);
return {static_cast<std::size_t>(matches.begin() - sorted_values.begin()),
        static_cast<std::size_t>(matches.end() - sorted_values.begin())};
```
