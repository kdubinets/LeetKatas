# Name

Partial Sort Smallest Prefix

# Description

Given a mutable integer vector and a valid `count <= values.size()`, place its smallest `count` elements in ascending order at the beginning. The remaining elements need not be sorted. This exercise covers partial ordering around an iterator boundary.

# Solution

```cpp
auto middle = values.begin() +
              static_cast<std::vector<int>::difference_type>(count);
std::ranges::partial_sort(values, middle);
```
