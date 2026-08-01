# Name

Maximum Array Value

# Description

Return the largest integer from a const, fixed-size `std::array<int, 5>`. The array is guaranteed nonempty by its type and must not be modified. This exercise covers retrieving an extremum from a range.

# Solution

```cpp
return *std::ranges::max_element(values);
```
