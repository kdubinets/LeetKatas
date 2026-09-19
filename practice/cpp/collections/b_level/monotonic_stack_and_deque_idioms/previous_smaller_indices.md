# Name

Nearest Strictly Smaller Index to the Left

# Description

Return the nearest earlier index holding a strictly smaller value for every position, or an empty optional if none exists. Equal values do not qualify. Preserve the input.

The supplied increasing candidate stack removes every non-smaller value before exposing the nearest strict boundary.

This exercise covers maintenance of a nearest strict monotonic boundary.

# Solution

```cpp
std::vector<std::optional<std::size_t>> result(values.size());
std::vector<std::size_t> candidates;
for (std::size_t index = 0; index < values.size(); ++index) {
    while (!candidates.empty() &&
           values[candidates.back()] >= values[index]) {
        candidates.pop_back();
    }
    if (!candidates.empty()) {
        result[index] = candidates.back();
    }
    candidates.push_back(index);
}
return result;
```
