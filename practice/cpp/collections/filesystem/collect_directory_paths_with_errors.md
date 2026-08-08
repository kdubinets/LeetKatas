# Name

Collect Directory Paths with Errors

# Description

Collect direct child paths without throwing. Construct and advance the directory iterator with the caller-provided error code, stop immediately on failure, and return any paths collected before an increment error.

# Solution

```cpp
std::vector<std::filesystem::path> result;
std::filesystem::directory_iterator it{directory, error};
const std::filesystem::directory_iterator end;
while (!error && it != end) {
    result.push_back(it->path());
    it.increment(error);
}
return result;
```
