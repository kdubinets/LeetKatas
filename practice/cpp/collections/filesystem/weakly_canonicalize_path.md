# Name

Weakly Canonicalize a Path

# Description

Return a normalized absolute path by canonicalizing the longest existing prefix and lexically processing any non-existing suffix. Use the throwing overload; unlike full canonicalization, the complete input need not exist.

# Solution

```cpp
return std::filesystem::weakly_canonical(value);
```
