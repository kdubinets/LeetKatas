# Name

Format a Named Measurement

# Description

Return a `std::string` containing a name, a colon and space, and a `double` rendered with exactly two fractional digits. This exercise covers combining differently typed arguments and a precision specifier in a compile-time-checked C++20 format string.

# Solution

```cpp
return std::format("{}: {:.2f}", name, value);
```
