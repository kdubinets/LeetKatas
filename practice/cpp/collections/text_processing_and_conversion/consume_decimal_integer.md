# Name

Consume a Decimal Integer

# Description

Parse an `int` from the beginning of a mutable `std::string_view`. On success, return the value and advance the view past exactly the consumed characters, leaving any suffix untouched. On invalid or out-of-range input, return an empty optional and leave the view unchanged. This exercise covers allocation-free prefix parsing with character conversion results.

# Solution

```cpp
if (remaining.empty()) {
    return std::nullopt;
}
int value;
auto [end, error] = std::from_chars(remaining.data(), remaining.data() + remaining.size(), value);
if (error != std::errc{}) {
    return std::nullopt;
}
remaining.remove_prefix(static_cast<std::size_t>(end - remaining.data()));
return value;
```
