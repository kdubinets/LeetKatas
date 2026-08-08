# Name

Remove a Path Tree

# Description

Recursively remove a path and all of its descendants through the non-throwing overload. Return the number of entries removed; the caller will inspect the supplied error code before using the count after a failure.

# Solution

```cpp
return std::filesystem::remove_all(value, error);
```
