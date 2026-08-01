# Name

Check All Strings Nonempty

# Description

Return whether every element of a const `std::vector<std::string>` is nonempty; an empty vector should satisfy the condition. This exercise covers a universal predicate check over a range.

# Solution

```cpp
return std::ranges::all_of(values, [](const std::string& value) {
    return !value.empty();
});
```
