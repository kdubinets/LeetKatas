# Name

Nearest Strictly Greater Index to the Right

# Description

Return the nearest later index holding a strictly greater value for every position, or an empty optional if none exists. Equal values do not qualify. Preserve the input.

The supplied decreasing stack contains unresolved indices; an arriving strictly greater value resolves indices from its top.

This exercise covers resolution of pending monotonic-stack indices with strict equality handling.

# Solution

```cpp
std::vector<std::optional<std::size_t>> result(values.size());
std::vector<std::size_t> pending;
for (std::size_t index = 0; index < values.size(); ++index) {
    while (!pending.empty() && values[pending.back()] < values[index]) {
        result[pending.back()] = index;
        pending.pop_back();
    }
    pending.push_back(index);
}
return result;
```
