# Name

Locate the First Regular-Expression Match

# Description

Search a const `std::string` with a precompiled `std::regex`. Return the zero-based position and length of the first match as `std::size_t` values, or an empty optional when no match exists. This exercise covers `std::regex_search`, `std::smatch`, and reading the overall match result.

# Solution

```cpp
std::smatch match;
if (!std::regex_search(text, match, pattern)) {
    return std::nullopt;
}
return std::pair{
    static_cast<std::size_t>(match.position()),
    static_cast<std::size_t>(match.length())};
```
