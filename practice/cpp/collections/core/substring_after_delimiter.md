# Name

Substring After Delimiter

# Description

Return the portion of a const `std::string` after its first occurrence of a supplied delimiter character. Return an empty string if the delimiter is missing; a delimiter at the end also produces an empty string. This exercise covers character search and substring extraction.

# Solution

```cpp
auto position = text.find(delimiter);
return position == std::string::npos ? std::string{}
                                     : text.substr(position + 1);
```
