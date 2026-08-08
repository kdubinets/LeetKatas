# Name

Query Available Filesystem Space

# Description

Query space information for the filesystem containing a path without throwing and return its `available` byte count. The caller must inspect the supplied error code before using the result after failure.

# Solution

```cpp
return std::filesystem::space(value, error).available;
```
