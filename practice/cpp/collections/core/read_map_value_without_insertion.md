# Name

Read Map Value Without Insertion

# Description

Look up a `std::string` key in a const `std::map<std::string, int>` and return its mapped integer as `std::optional<int>`, leaving the map unchanged and returning an empty optional for a missing key. This exercise covers non-inserting associative lookup.

# Solution

```cpp
auto it = values.find(key);
return it == values.end() ? std::nullopt : std::optional<int>{it->second};
```
