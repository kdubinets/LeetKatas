# Name

Extract a Regular-Expression Capture

# Description

Search a const `std::string` with a precompiled `std::regex` and return one capture from the first match. The zero-based `group` index uses zero for the overall match; return an empty optional when there is no match, the index is unavailable, or an optional capture did not participate. This exercise covers safe indexed access to `std::smatch` results.

# Solution

```cpp
std::smatch match;
if (!std::regex_search(text, match, pattern)
    || group >= match.size()
    || !match[group].matched) {
    return std::nullopt;
}
return match[group].str();
```
