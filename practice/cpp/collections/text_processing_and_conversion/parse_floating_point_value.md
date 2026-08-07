# Name

Parse a Complete Floating-Point Value

# Description

Parse a `double` from a `std::string_view` using the general floating-point syntax. Return the value only when conversion succeeds and consumes the complete input; invalid, trailing, or out-of-range input returns an empty optional. This exercise covers allocation-free floating-point `std::from_chars` conversion.

# Solution

```cpp
if (text.empty()) {
    return std::nullopt;
}
double value;
auto [end, error] = std::from_chars(
    text.data(), text.data() + text.size(), value, std::chars_format::general);
if (error != std::errc{} || end != text.data() + text.size()) {
    return std::nullopt;
}
return value;
```
