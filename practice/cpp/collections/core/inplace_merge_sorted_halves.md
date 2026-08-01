# Name

In-Place Merge Sorted Halves

# Description

Given a mutable integer vector and a valid boundary `middle <= values.size()`, merge the adjacent sorted ranges `[0, middle)` and `[middle, values.size())` into one ascending range in the same vector. This exercise covers in-place merging around an iterator boundary.

# Solution

```cpp
auto boundary = values.begin() +
                static_cast<std::vector<int>::difference_type>(middle);
std::ranges::inplace_merge(values, boundary);
```
