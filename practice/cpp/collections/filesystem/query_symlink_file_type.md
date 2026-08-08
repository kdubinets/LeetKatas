# Name

Query a Symlink's Own Type

# Description

Return the `file_type` of the directory entry named by a path without following a symbolic link to its target. Use the throwing status query designed for inspecting the link itself.

# Solution

```cpp
return std::filesystem::symlink_status(value).type();
```
