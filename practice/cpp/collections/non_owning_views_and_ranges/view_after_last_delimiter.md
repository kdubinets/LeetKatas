# Name

View After the Last Delimiter

# Description

Return a non-owning view of the characters after the final occurrence of a delimiter. If the delimiter is absent, return the complete input view; a trailing delimiter produces an empty view. This exercise covers reverse search followed by allocation-free slicing.

# Solution

```cpp
auto position = text.rfind(delimiter);
return position == std::string_view::npos ? text : text.substr(position + 1);
```
