# Name

Collect Recursive Paths

# Description

Traverse every descendant beneath a directory recursively and return each visited entry's full path. Preserve recursive iterator order, do not include the root itself, and allow filesystem exceptions to propagate.

# Solution

```cpp
std::vector<std::filesystem::path> result;
for (const auto& entry
     : std::filesystem::recursive_directory_iterator{directory}) {
    result.push_back(entry.path());
}
return result;
```
