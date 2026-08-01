# Name

Insert Unordered Set Value

# Description

Insert a string into a mutable `std::unordered_set<std::string>` and return whether the set changed because the value was new. This exercise covers interpreting the result of unique-key insertion.

# Solution

```cpp
return values.insert(value).second;
```
