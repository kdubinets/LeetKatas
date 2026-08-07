# Name

Parse a Complete Hexadecimal Integer

# Description

Parse an `unsigned int` from hexadecimal digits in a `std::string_view`. Return the value only when conversion succeeds and consumes the entire nonempty input; prefixes such as `0x`, trailing characters, invalid input, and out-of-range values must produce an empty optional. This exercise covers base-specific `std::from_chars` parsing and complete-consumption validation.

# Solution

```cpp
if (text.empty()) {
    return std::nullopt;
}
unsigned int value;
auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value, 16);
if (error != std::errc{} || end != text.data() + text.size()) {
    return std::nullopt;
}
return value;
```
