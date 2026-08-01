# Name

Check Sorted Multiset Includes

# Description

Given two const ascending integer vectors, return whether the first contains every value occurrence required by the second. Duplicate multiplicities matter, and neither input may be modified. This exercise covers containment testing between sorted ranges.

# Solution

```cpp
return std::ranges::includes(values, required);
```
