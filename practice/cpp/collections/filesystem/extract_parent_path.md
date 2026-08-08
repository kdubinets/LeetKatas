# Name

Extract a Parent Path

# Description

Return the lexical parent portion of a const path without accessing the filesystem. The result excludes the final filename component and follows standard root and trailing-separator behavior.

# Solution

```cpp
return value.parent_path();
```
