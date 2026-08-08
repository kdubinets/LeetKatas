# Name

Make an Absolute Path

# Description

Return an absolute form of a path using the standard filesystem resolution context. The path need not exist, and failures from the throwing overload may propagate.

# Solution

```cpp
return std::filesystem::absolute(value);
```
