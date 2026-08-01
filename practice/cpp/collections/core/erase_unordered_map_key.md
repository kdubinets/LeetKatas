# Name

Erase Unordered Map Key

# Description

Remove a string key and its mapped integer from a mutable `std::unordered_map`, returning whether an entry existed and was erased. All other entries remain unchanged. This exercise covers key-based associative erasure and interpreting its count.

# Solution

```cpp
return values.erase(key) != 0;
```
