# Name

Write an Integer into Existing Storage

# Description

Write the decimal representation of an `int` into a mutable `std::span<char>` without adding a null terminator. Return the number of characters written, or an empty optional when the destination is too small; do not write beyond the span. This exercise covers capacity-aware `std::to_chars` output into caller-owned storage.

# Solution

```cpp
if (output.empty()) {
    return std::nullopt;
}
auto [end, error] = std::to_chars(output.data(), output.data() + output.size(), value);
if (error != std::errc{}) {
    return std::nullopt;
}
return static_cast<std::size_t>(end - output.data());
```
