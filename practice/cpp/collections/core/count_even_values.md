# Name

Count Even Values

# Description

Count the even integers in a const `std::vector<int>` and return the count as `std::size_t`, without modifying the vector. This exercise covers predicate-based counting and sensible count conversion.

# Solution

```cpp
return static_cast<std::size_t>(
    std::ranges::count_if(values, [](int value) { return value % 2 == 0; }));
```
