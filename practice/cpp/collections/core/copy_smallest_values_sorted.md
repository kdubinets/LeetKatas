# Name

Copy Smallest Values Sorted

# Description

Given a const integer vector and a valid `count <= values.size()`, return its smallest `count` values in ascending order without modifying the input. The result is already sized. This exercise covers non-mutating partial sorting into a bounded output range.

# Solution

```cpp
std::ranges::partial_sort_copy(values, result);
```
