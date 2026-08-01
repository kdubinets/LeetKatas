# Name

Insert into Sorted Vector

# Description

Insert an integer into a mutable ascending vector while preserving its ordering, placing the new value before any existing equal values. This exercise covers coupling a binary-search boundary with sequence insertion.

# Solution

```cpp
auto position = std::ranges::lower_bound(sorted_values, value);
sorted_values.insert(position, value);
```
