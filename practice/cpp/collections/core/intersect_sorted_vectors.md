# Name

Intersect Sorted Vectors

# Description

Given two const ascending integer vectors, return their ascending multiset intersection. Each value must appear in the result the minimum number of times it appears in either input. This exercise covers a sorted set-style algorithm with duplicate semantics.

# Solution

```cpp
std::ranges::set_intersection(left, right, std::back_inserter(result));
```
