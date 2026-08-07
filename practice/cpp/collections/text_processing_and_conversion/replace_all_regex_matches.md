# Name

Replace All Regular-Expression Matches

# Description

Return a new `std::string` in which every non-overlapping match of a precompiled `std::regex` is replaced using the supplied replacement text. Leave the input string unchanged; replacement references such as `$1` retain their standard meaning. This exercise covers the default all-match behavior of standard regular-expression replacement.

# Solution

```cpp
return std::regex_replace(text, pattern, replacement);
```
