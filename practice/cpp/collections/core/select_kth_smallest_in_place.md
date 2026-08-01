# Name

Select Kth Smallest In Place

# Description

Given a mutable nonempty integer vector and a valid zero-based `std::size_t` index `k`, rearrange the vector as needed and return the value that a full ascending sort would place at `k`. Complete sorting is not required. This exercise covers in-place order-statistic selection.

# Solution

```cpp
auto nth = values.begin() + static_cast<std::vector<int>::difference_type>(k);
std::ranges::nth_element(values, nth);
return *nth;
```
