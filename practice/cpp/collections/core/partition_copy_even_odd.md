# Name

Partition-Copy Even and Odd Values

# Description

Copy a const integer vector into a pair of output vectors, placing even values in the first and odd values in the second while preserving relative order within each group. The input must remain unchanged. This exercise covers splitting a range into two output iterators with one predicate.

# Solution

```cpp
std::ranges::partition_copy(values,
                            std::back_inserter(result.first),
                            std::back_inserter(result.second),
                            [](int value) { return value % 2 == 0; });
```
