# Name

Create Nested Directories

# Description

Create all missing directory components in a path without throwing. Return `true` only when at least one directory was created, return `false` when the full path already existed, and expose failures through `error`.

# Solution

```cpp
return std::filesystem::create_directories(value, error);
```
