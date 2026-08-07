# Name

Consume a String View Token

# Description

Return the portion of a mutable `std::string_view` before its next delimiter, then advance the input view beyond that delimiter. If no delimiter exists, return all remaining text and leave the input empty. Empty tokens are preserved. This exercise covers allocation-free incremental token parsing.

# Solution

```cpp
auto position = remaining.find(delimiter);
auto token = remaining.substr(0, position);
if (position == std::string_view::npos) {
    remaining = {};
} else {
    remaining.remove_prefix(position + 1);
}
return token;
```
