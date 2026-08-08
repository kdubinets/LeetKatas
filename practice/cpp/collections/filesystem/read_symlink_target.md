# Name

Read a Symbolic Link Target

# Description

Return the path stored in a symbolic link without following it to its target. Use the non-throwing operation and report failures through the caller-provided error code; the returned path may be relative to the link's parent.

# Solution

```cpp
return std::filesystem::read_symlink(value, error);
```
