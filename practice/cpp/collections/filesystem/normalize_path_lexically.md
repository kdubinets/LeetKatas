# Name

Normalize a Path Lexically

# Description

Return a lexically normalized path that removes redundant separators and dot components and resolves parent components where possible. Do not query the filesystem, resolve symlinks, or require the path to exist.

# Solution

```cpp
return value.lexically_normal();
```
