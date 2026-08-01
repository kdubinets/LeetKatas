# Name

Insert or Assign Map Value

# Description

Store an integer under a string key in a mutable ordered map, replacing the mapped value if the key already exists. Return true only when a new key was inserted. This exercise covers associative insert-or-overwrite behavior and its result.

# Solution

```cpp
return values.insert_or_assign(key, value).second;
```
