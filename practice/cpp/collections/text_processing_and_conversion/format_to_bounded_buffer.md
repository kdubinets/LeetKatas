# Name

Format into Bounded Storage

# Description

Format an `int` as decimal text into a mutable `std::span<char>` without writing beyond its capacity or adding a null terminator. Return the number of characters actually written and the total number required for complete output. This exercise covers bounded C++20 formatted output and interpreting its size result when truncation occurs.

# Solution

```cpp
auto capacity = std::ssize(output);
auto result = std::format_to_n(output.begin(), capacity, "{}", value);
auto required = static_cast<std::size_t>(result.size);
return {
    static_cast<std::size_t>(std::min(capacity, result.size)),
    required};
```
