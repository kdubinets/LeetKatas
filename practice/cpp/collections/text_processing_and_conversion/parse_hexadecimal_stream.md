# Name

Parse Hexadecimal Stream Input

# Description

Read the leading hexadecimal `unsigned int` from a `std::string_view` using stream extraction, accepting the conventional optional base prefix. Return an empty optional if no value can be extracted; trailing input may remain. This exercise covers changing a stream's integer base before typed extraction.

# Solution

```cpp
std::istringstream input{std::string{text}};
unsigned int value;
if (input >> std::hex >> value) {
    return value;
}
return std::nullopt;
```
