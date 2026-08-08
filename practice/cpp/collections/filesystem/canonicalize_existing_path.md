# Name

Canonicalize an Existing Path

# Description

Return the absolute canonical path for an existing filesystem object, resolving dot components and symbolic links. Use the non-throwing overload and report failure through the caller-provided error code.

# Solution

```cpp
return std::filesystem::canonical(value, error);
```
