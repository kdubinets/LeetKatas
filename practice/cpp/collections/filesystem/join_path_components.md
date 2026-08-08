# Name

Join Path Components

# Description

Return a new `std::filesystem::path` formed by joining `child` beneath `base` with platform-aware path semantics. Neither input may be modified; if `child` is absolute, standard path-append replacement behavior applies.

# Solution

```cpp
return base / child;
```
