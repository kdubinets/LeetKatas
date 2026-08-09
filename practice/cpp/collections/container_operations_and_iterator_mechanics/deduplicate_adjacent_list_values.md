# Name

Deduplicate Adjacent List Values

# Description

For each run of adjacent equal integers in a mutable `std::list<int>`, retain its first node and remove the rest. Return the number of removed nodes. Values that are equal but separated must remain. This exercise covers list-owned adjacent deduplication and its C++20 count result.

# Solution

```cpp
return values.unique();
```
