# Name

Collect Path Components

# Description

Iterate over a const `std::filesystem::path` and return its component paths in native path order. Root names, root directories, filenames, and relative components must follow the path iterator's standard decomposition.

# Solution

```cpp
return std::vector<std::filesystem::path>(
    value.begin(), value.end());
```
