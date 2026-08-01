# Name

Stable Partition Negatives

# Description

Reorder a mutable `std::vector<int>` so all negative values precede all nonnegative values, preserving the original relative order inside each group. This exercise covers stable predicate-based partitioning.

# Solution

```cpp
std::stable_partition(values.begin(), values.end(),
                      [](int value) { return value < 0; });
```
