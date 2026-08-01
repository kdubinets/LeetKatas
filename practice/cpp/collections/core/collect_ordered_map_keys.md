# Name

Collect Ordered Map Keys

# Description

Return a vector containing every key from a const `std::map<int, int>` in the map's ascending iteration order, without copying mapped values or modifying the map. The result capacity is already reserved. This exercise covers extracting keys while iterating associative entries.

# Solution

```cpp
for (const auto& entry : values) {
    keys.push_back(entry.first);
}
```
