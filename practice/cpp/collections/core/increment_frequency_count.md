# Name

Increment Frequency Count

# Description

Update a mutable `std::unordered_map<std::string, int>` so the supplied word's count increases by one, with an absent word acquiring a count of one. This exercise covers intentional insertion through mapped-value access.

# Solution

```cpp
++frequencies[word];
```
