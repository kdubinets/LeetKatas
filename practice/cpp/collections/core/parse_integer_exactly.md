# Name

Parse Integer Exactly

# Description

Parse a non-owning character sequence as a base-10 `int`, returning an empty optional for an empty input, invalid syntax, overflow, or trailing characters. Leading whitespace and a leading plus sign are not accepted. This exercise covers allocation-free numeric conversion with complete-consumption validation.

# Solution

```cpp
if (text.empty()) {
    return std::nullopt;
}
int value = 0;
const char* end = text.data() + text.size();
auto [position, error] = std::from_chars(text.data(), end, value);
if (error != std::errc{} || position != end) {
    return std::nullopt;
}
return value;
```
