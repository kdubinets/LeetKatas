# Name

Insert Map Entry If Absent

# Description

Add a `std::string` key and integer value to a mutable `std::map` only if that key is not already present, preserving any existing mapped value. Return whether a new entry was inserted. This exercise covers conditional associative insertion and its result.

# Solution

```cpp
return values.try_emplace(key, initial_value).second;
```
