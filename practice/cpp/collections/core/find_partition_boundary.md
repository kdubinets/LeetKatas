# Name

Find Partition Boundary

# Description

Given a const integer vector partitioned with all negative values before all nonnegative values, return the `std::size_t` index of the first nonnegative value, or the vector size if every value is negative. This exercise covers locating the boundary of a predicate-partitioned range.

# Solution

```cpp
auto boundary = std::ranges::partition_point(
    values, [](int value) { return value < 0; });
return static_cast<std::size_t>(boundary - values.begin());
```
