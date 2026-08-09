# Name

Open a Binary File at the End

# Description

Open `path` as a binary C++ input file whose initial read position is immediately after its contents. Return the move-only `std::ifstream` in an optional on success, or an empty optional on open failure. This exercise covers combining binary and initial-at-end file modes for later size or random-access work.

# Solution

```cpp
std::ifstream input{path, std::ios::in | std::ios::binary | std::ios::ate};
if (!input.is_open()) {
    return std::nullopt;
}
return std::optional<std::ifstream>{std::move(input)};
```
