# Name

Erase Odd Vector Values

# Description

Mutate a `std::vector<int>` by removing all odd elements while preserving the relative order of the even elements. This exercise covers concise predicate-based sequence erasure.

# Solution

```cpp
std::erase_if(values, [](int value) { return value % 2 != 0; });
```
