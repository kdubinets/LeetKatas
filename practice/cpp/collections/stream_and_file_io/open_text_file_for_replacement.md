# Name

Open a Text File for Replacement

# Description

Open `path` as a C++ text output file with an explicit contract that any existing contents are discarded before new output is written. Return the move-only `std::ofstream` in an optional on success, or an empty optional on open failure. This exercise covers deliberate truncation rather than accidental reliance on a default output mode.

# Solution

```cpp
std::ofstream output{path, std::ios::out | std::ios::trunc};
if (!output.is_open()) {
    return std::nullopt;
}
return std::optional<std::ofstream>{std::move(output)};
```
