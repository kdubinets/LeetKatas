# Name

Convert an Integer to Hexadecimal Text

# Description

Return an `unsigned int` as lowercase hexadecimal digits in a `std::string`, with no `0x` prefix. Use a bounded local character buffer rather than a stream. This exercise covers base-specific integer `std::to_chars` conversion.

# Solution

```cpp
std::array<char, (std::numeric_limits<unsigned int>::digits + 3) / 4> buffer{};
auto result = std::to_chars(buffer.data(), buffer.data() + buffer.size(), value, 16);
return {buffer.data(), result.ptr};
```
