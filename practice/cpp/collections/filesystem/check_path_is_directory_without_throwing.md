# Name

Check for a Directory Without Throwing

# Description

Return whether a path resolves to a directory through the non-throwing convenience query. Place any filesystem failure in the caller-provided `std::error_code`, which the caller will inspect before trusting `false`.

# Solution

```cpp
return std::filesystem::is_directory(value, error);
```
