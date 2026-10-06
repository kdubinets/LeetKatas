# Name

Answer Inclusive Range Sums

# Description

Return one sum per query, in query order. Each pair `{first, last}` requests the sum of elements in `values` from index `first` through `last`, including both endpoints. Every range satisfies `first <= last < values.size()`. An empty query list produces an empty result. Preserve both inputs, and assume all prefix and range sums fit in long long.

The supplied pattern is one-past prefix sums: each prefix position represents the total before that position, and an inclusive range sum is the difference between its two boundary prefixes.

This exercise covers answering inclusive range queries from a one-past prefix-sum representation.

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
