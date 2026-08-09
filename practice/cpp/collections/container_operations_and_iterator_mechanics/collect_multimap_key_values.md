# Name

Collect Multimap Key Values

# Description

Return every `std::string` mapped to `key` in a const `std::multimap<int, std::string>`, preserving the container's iteration order for equivalent keys. Return an empty vector when the key is absent and do not modify the map. This exercise covers retrieving the complete equivalent-key range from a multimap.

# Solution

```cpp
std::vector<std::string> result;
auto [first, last] = values.equal_range(key);
for (auto it = first; it != last; ++it) {
    result.push_back(it->second);
}
return result;
```
