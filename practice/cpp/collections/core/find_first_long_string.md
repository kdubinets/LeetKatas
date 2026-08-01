# Name

Find First Long String

# Description

Search a const vector of strings and return a copy of the first string whose length is at least the supplied `std::size_t` threshold, or an empty `std::optional<std::string>` when there is no match. This exercise covers predicate search and optional results.

# Solution

```cpp
auto it = std::ranges::find_if(values, [minimum_length](const std::string& value) {
    return value.size() >= minimum_length;
});
return it == values.end() ? std::nullopt
                          : std::optional<std::string>{*it};
```
