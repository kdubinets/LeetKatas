# Name

Sort Pairs by Score Then ID

# Description

Sort a mutable vector of `(id, score)` integer pairs in place, placing higher scores first and smaller IDs first when scores tie. This exercise covers a custom comparator with a two-field strict ordering.

# Solution

```cpp
std::ranges::sort(records, [](const auto& a, const auto& b) {
    return a.second != b.second ? a.second > b.second : a.first < b.first;
});
```
