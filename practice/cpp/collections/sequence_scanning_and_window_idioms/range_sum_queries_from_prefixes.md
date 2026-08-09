# Name

Answer Inclusive Range Sums

# Description

Use one-past prefix sums to answer every inclusive `[first, second]` query over `values`. Every supplied index pair is valid and ordered. Build the prefix representation once, then use the difference between the prefix after `second` and the prefix at `first` for each answer.

# Solution

```cpp
std::vector<long long> prefixes(values.size() + 1, 0);
for (std::size_t index = 0; index < values.size(); ++index) {
    prefixes[index + 1] = prefixes[index] + values[index];
}

std::vector<long long> result;
result.reserve(queries.size());
for (const auto& [first, second] : queries) {
    result.push_back(prefixes[second + 1] - prefixes[first]);
}
return result;
```
