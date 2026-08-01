# Name

Merge Sorted Vectors

# Description

Combine two const ascending integer vectors into one ascending result vector, retaining all duplicate values and leaving both inputs unchanged. The destination capacity is already reserved. This exercise covers merging two sorted ranges into an output iterator.

# Solution

```cpp
std::ranges::merge(left, right, std::back_inserter(result));
```
