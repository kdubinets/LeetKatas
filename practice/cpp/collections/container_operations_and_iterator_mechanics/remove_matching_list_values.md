# Name

Remove Matching List Values

# Description

Remove every integer less than `limit` from a mutable `std::list<int>`, preserve the order of retained nodes, and return the number removed. This exercise covers list-owned predicate removal and its C++20 count result.

# Solution

```cpp
return values.remove_if([limit](int value) { return value < limit; });
```
