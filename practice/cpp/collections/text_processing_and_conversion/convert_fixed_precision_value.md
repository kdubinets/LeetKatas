# Name

Convert a Fixed-Precision Value

# Description

Convert a finite `double` to fixed-point text with exactly the requested number of digits after the decimal point. The caller guarantees a precision from 0 through 20, so the provided local capacity is sufficient. This exercise covers the floating-point format and precision overload of `std::to_chars`.

# Solution

```cpp
std::array<char, 384> buffer{};
auto result = std::to_chars(
    buffer.data(), buffer.data() + buffer.size(), value, std::chars_format::fixed, precision);
return {buffer.data(), result.ptr};
```
