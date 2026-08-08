# Name

Copy a Directory Tree

# Description

Copy a source directory and all descendants to a destination without throwing. Enable recursive traversal, replace existing regular destination files when permitted, and report failures through the caller-provided error code.

# Solution

```cpp
std::filesystem::copy(
    source,
    destination,
    std::filesystem::copy_options::recursive
        | std::filesystem::copy_options::overwrite_existing,
    error);
```
