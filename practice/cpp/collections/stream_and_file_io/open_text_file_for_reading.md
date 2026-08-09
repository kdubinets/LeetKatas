# Name

Open a Text File for Reading

# Description

Open `path` as a C++ text input file. Return the move-only `std::ifstream` in an optional when it opens successfully, or an empty optional on open failure. This exercise covers explicit file-open validation while transferring ownership of the stream to the caller.

# Solution

```cpp
std::ifstream input{path};
if (!input.is_open()) {
    return std::nullopt;
}
return std::optional<std::ifstream>{std::move(input)};
```
