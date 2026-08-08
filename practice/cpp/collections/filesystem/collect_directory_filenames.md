# Name

Collect Directory Filenames

# Description

Iterate over the direct children of a directory and return only each entry's filename component as a path. Preserve iterator order, which is unspecified by the standard, and allow filesystem exceptions to propagate.

# Solution

```cpp
std::vector<std::filesystem::path> result;
for (const auto& entry : std::filesystem::directory_iterator{directory}) {
    result.push_back(entry.path().filename());
}
return result;
```
