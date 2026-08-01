# Name

Trim ASCII Whitespace View

# Description

Return a `std::string_view` excluding leading and trailing ASCII space, tab, newline, carriage-return, form-feed, and vertical-tab characters. An all-whitespace input produces an empty view, and no characters are copied or modified. This exercise covers safely narrowing non-owning string boundaries.

# Solution

```cpp
constexpr char whitespace_characters[] = {' ', 9, 10, 11, 12, 13};
const std::string_view whitespace{whitespace_characters,
                                  sizeof(whitespace_characters)};
auto first = text.find_first_not_of(whitespace);
if (first == std::string_view::npos) {
    return {};
}
auto last = text.find_last_not_of(whitespace);
return text.substr(first, last - first + 1);
```
