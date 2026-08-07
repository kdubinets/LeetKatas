# Name

Classify an Integer Parse

# Description

Classify a `std::string_view` intended to contain one complete decimal `int`. Distinguish input that starts invalidly, a digit sequence outside the `int` range, an in-range value followed by trailing characters, and complete success. An out-of-range digit sequence remains `out_of_range` even when trailing characters follow it. This exercise covers interpreting `std::from_chars` error codes and its returned end pointer.

# Solution

```cpp
if (text.empty()) {
    return ParseResult::invalid;
}
int value;
auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
if (error == std::errc::invalid_argument) {
    return ParseResult::invalid;
}
if (error == std::errc::result_out_of_range) {
    return ParseResult::out_of_range;
}
if (end != text.data() + text.size()) {
    return ParseResult::trailing_characters;
}
return ParseResult::success;
```
