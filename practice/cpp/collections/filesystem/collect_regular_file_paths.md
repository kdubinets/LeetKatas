# Name

Collect Regular File Paths

# Description

Iterate over a directory's direct entries and return the full path of each entry whose resolved status is a regular file. Preserve iterator order and allow filesystem exceptions to propagate.

# Solution

```cpp
std::vector<std::filesystem::path> result;
for (const auto& entry : std::filesystem::directory_iterator{directory}) {
    if (entry.is_regular_file()) {
        result.push_back(entry.path());
    }
}
return result;
```
