# Name

Union Sorted Vectors

# Description

Given two const ascending integer vectors, return their ascending multiset union. Each value must appear the maximum number of times it appears in either input. This exercise covers sorted union with duplicate-count semantics.

# Solution

```cpp
std::ranges::set_union(left, right, std::back_inserter(result));
```
