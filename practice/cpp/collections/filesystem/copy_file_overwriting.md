# Name

Copy a File with Overwrite

# Description

Copy one regular file to a destination without throwing, replacing an existing destination file when permitted. Return whether a copy occurred and report failures through the caller-provided error code.

# Solution

```cpp
return std::filesystem::copy_file(
    source,
    destination,
    std::filesystem::copy_options::overwrite_existing,
    error);
```
