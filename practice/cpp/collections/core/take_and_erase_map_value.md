# Name

Take and Erase Map Value

# Description

Find an integer key in a mutable map, move its mapped string into an optional result, and erase the entry. Return an empty optional for a missing key. This exercise covers a tightly coupled lookup, move, and iterator-safe erasure pattern.

# Solution

```cpp
auto it = values.find(key);
if (it == values.end()) {
    return std::nullopt;
}
std::optional<std::string> result{std::move(it->second)};
values.erase(it);
return result;
```
