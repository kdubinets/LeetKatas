# Name

Add Path Permissions

# Description

Add the supplied permission bits to a filesystem entry while preserving all existing bits. Use the non-throwing overload and the permission option that performs an additive update; failures are returned in `error`.

# Solution

```cpp
std::filesystem::permissions(
    value,
    additions,
    std::filesystem::perm_options::add,
    error);
```
