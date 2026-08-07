# Name

Extract Quoted Text

# Description

Extract one leading double-quoted field from a `std::string_view`, removing its delimiters and decoding the escape mechanism used by `std::quoted`. Return an empty optional when the first field is not quoted or extraction fails; trailing input may remain. This exercise covers validating and extracting `std::quoted` input.

# Solution

```cpp
std::istringstream input{std::string{text}};
input >> std::ws;
if (input.peek() != '"') {
    return std::nullopt;
}
std::string value;
if (input >> std::quoted(value)) {
    return value;
}
return std::nullopt;
```
