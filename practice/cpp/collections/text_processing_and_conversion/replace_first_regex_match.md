# Name

Replace the First Regular-Expression Match

# Description

Return a new `std::string` in which only the first match of a precompiled `std::regex` is replaced using the supplied replacement text. Leave later matches and the input string unchanged. This exercise covers applying the standard first-only replacement format flag.

# Solution

```cpp
return std::regex_replace(
    text, pattern, replacement, std::regex_constants::format_first_only);
```
