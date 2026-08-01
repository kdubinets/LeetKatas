# Name

Weighted Sum of Map Entries

# Description

For a const `std::map<int, int>`, calculate a `long long` total of every key multiplied by its mapped value. This exercise covers iterating associative entries with structured bindings while widening arithmetic appropriately.

# Solution

```cpp
for (const auto& [key, value] : weights) {
    total += static_cast<long long>(key) * value;
}
```
