# Name

Extract a Path Filename

# Description

Return the final filename component of a const `std::filesystem::path` as another path. Preserve the standard lexical behavior for paths ending in a directory separator or containing only a root.

# Solution

```cpp
return value.filename();
```
