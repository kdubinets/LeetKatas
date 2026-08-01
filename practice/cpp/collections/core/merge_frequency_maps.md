# Name

Merge Frequency Maps

# Description

Add all counts from a const `std::unordered_map<std::string, int>` into a mutable frequency map, inserting keys that are not already present. The additional map must remain unchanged. This exercise covers associative iteration and intentional mapped-value insertion during aggregation.

# Solution

```cpp
for (const auto& [word, count] : additional) {
    frequencies[word] += count;
}
```
