# Name

Skip Named Directory Subtrees

# Description

Recursively collect descendant paths, including matching directory entries themselves, but do not visit children of a directory whose filename equals `skipped_name`. Preserve iterator order and allow filesystem exceptions to propagate.

# Solution

```cpp
std::vector<std::filesystem::path> result;
std::filesystem::recursive_directory_iterator it{directory};
const std::filesystem::recursive_directory_iterator end;
for (; it != end; ++it) {
    result.push_back(it->path());
    if (it->is_directory() && it->path().filename() == skipped_name) {
        it.disable_recursion_pending();
    }
}
return result;
```
