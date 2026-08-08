# Name

Query Last Write Time

# Description

Read a path's last modification time as `std::filesystem::file_time_type` through the non-throwing overload. The caller will inspect `error` before using the returned sentinel value after failure.

# Solution

```cpp
return std::filesystem::last_write_time(value, error);
```
