# Name

Query a Path's File Type

# Description

Return the `std::filesystem::file_type` for the object reached by a path, following a symlink when present. Use the throwing query; filesystem failures may propagate as `filesystem_error`.

# Solution

```cpp
return std::filesystem::status(value).type();
```
