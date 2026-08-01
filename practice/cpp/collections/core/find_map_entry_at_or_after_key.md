# Name

Find Map Entry at or After Key

# Description

In a const ordered `std::map<int, int>`, find the first `(key, value)` entry whose key is at least the supplied key and return it as an optional pair. Return an empty optional if no qualifying entry exists. This exercise covers ordered associative boundary lookup.

# Solution

```cpp
auto it = values.lower_bound(key);
return it == values.end()
           ? std::nullopt
           : std::optional<std::pair<int, int>>{*it};
```
