# Name

Remove One Path

# Description

Remove one file, symlink, or empty directory through the non-throwing overload. Return whether an entry was removed, return `false` when it did not exist, and expose failures through the caller's error code.

# Solution

```cpp
return std::filesystem::remove(value, error);
```
