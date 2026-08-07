# Name

Parse a Textual Boolean

# Description

Parse a complete `std::string_view` containing the stream Boolean words `true` or `false`. Return the corresponding `bool`; malformed input or non-whitespace trailing characters returns an empty optional. This exercise covers enabling textual Boolean extraction and validating the remaining stream input.

# Solution

```cpp
std::istringstream input{std::string{text}};
bool value;
if (!(input >> std::boolalpha >> value)) {
    return std::nullopt;
}
char trailing;
if (input >> trailing) {
    return std::nullopt;
}
return value;
```
