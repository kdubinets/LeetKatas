# Name

Check Path Equivalence

# Description

Return whether two paths resolve to the same existing filesystem object, rather than merely comparing their spelling. Use the non-throwing overload and report query failures through the caller's error code.

# Solution

```cpp
return std::filesystem::equivalent(left, right, error);
```
