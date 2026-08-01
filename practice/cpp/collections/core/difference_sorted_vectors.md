# Name

Difference of Sorted Vectors

# Description

Given two const ascending integer vectors, return the ascending multiset difference of the left input minus the right. Each right occurrence removes at most one equal left occurrence. This exercise covers sorted difference with duplicate-count semantics.

# Solution

```cpp
std::ranges::set_difference(left, right, std::back_inserter(result));
```
