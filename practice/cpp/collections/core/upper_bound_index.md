# Name

Upper Bound Index

# Description

Given a const ascending `std::vector<int>`, return the `std::size_t` index of the first element strictly greater than the target, or the vector size if no such element exists. This exercise covers the upper insertion boundary and iterator-to-index conversion.

# Solution

```cpp
return static_cast<std::size_t>(
    std::ranges::upper_bound(sorted_values, target) - sorted_values.begin());
```
