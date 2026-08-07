# Name

Convert an Integer to Decimal Text

# Description

Return the ordinary decimal representation of an `int` as a `std::string`, including a leading minus sign for negative values. Use a bounded local character buffer without a stream or intermediate formatted allocation. This exercise covers integer `std::to_chars` conversion and constructing text from its returned boundary.

# Solution

```cpp
std::array<char, 32> buffer{};
auto result = std::to_chars(buffer.data(), buffer.data() + buffer.size(), value);
return {buffer.data(), result.ptr};
```
