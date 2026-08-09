# Name

Open a Text File for Appending

# Description

Open `path` as a C++ text output file so existing contents are preserved and every write goes at the end. Return the move-only `std::ofstream` in an optional on success, or an empty optional on open failure. This exercise covers selecting append mode and explicitly reporting file-open status.

# Solution

```cpp
std::ofstream output{path, std::ios::out | std::ios::app};
if (!output.is_open()) {
    return std::nullopt;
}
return std::optional<std::ofstream>{std::move(output)};
```
