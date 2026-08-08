# Name

Rename a Path Without Throwing

# Description

Rename or move a filesystem entry from `source` to `destination` through the non-throwing overload. Return a default error code on success or the reported failure code otherwise.

# Solution

```cpp
std::error_code error;
std::filesystem::rename(source, destination, error);
return error;
```
