# Name

Lower Bound Index

# Description

Given a const ascending `std::vector<int>`, return the `std::size_t` index of the first element that is not less than the target, or the vector size if no such element exists. This exercise covers binary-search iterators and iterator-distance conversion.

# Solution

```cpp
return static_cast<std::size_t>(
    std::ranges::lower_bound(sorted_values, target) - sorted_values.begin());
```
