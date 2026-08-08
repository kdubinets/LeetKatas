# Name

Make a Filesystem-Relative Path

# Description

Return `value` relative to `base` after filesystem-aware weak canonicalization. Use the non-throwing overload and expose resolution failures through the supplied error code; this differs from purely lexical relativity.

# Solution

```cpp
return std::filesystem::relative(value, base, error);
```
