# Name

Find Minimum and Maximum

# Description

Given a nonempty const integer vector, return a `std::pair<int, int>` containing its minimum followed by its maximum, without modifying the vector. This exercise covers obtaining both extrema and packaging a pair result.

# Solution

```cpp
auto [minimum, maximum] = std::ranges::minmax_element(values);
return {*minimum, *maximum};
```
