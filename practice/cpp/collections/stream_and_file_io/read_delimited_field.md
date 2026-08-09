# Name

Read a Delimited Field

# Description

Read characters from a caller-provided `std::istream&` through the next occurrence of `delimiter`, excluding that delimiter from the result. An immediately encountered delimiter produces a present empty string; return an empty optional only when no field can be read. This exercise covers delimiter-selected unformatted stream input.

# Solution

```cpp
std::string field;
if (std::getline(input, field, delimiter)) {
    return field;
}
return std::nullopt;
```
