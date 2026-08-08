# Name

Propagate a Filesystem Error Code

# Description

Query a path's file size through a non-throwing filesystem overload. Return the size when successful or the resulting `std::error_code` when the operation fails.

# Solution

```cpp
std::error_code error;
const auto size = std::filesystem::file_size(path, error);
if (error) {
    return error;
}
return size;
```
