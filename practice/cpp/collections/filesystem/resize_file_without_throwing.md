# Name

Resize a File Without Throwing

# Description

Change a regular file to the requested byte size through the non-throwing operation. Truncate it when the size decreases, extend it according to filesystem semantics when the size increases, and report failures through the supplied error code.

# Solution

```cpp
std::filesystem::resize_file(value, size, error);
```
