# Name

Check Vector Sorted

# Description

Return whether a const integer vector is in nondecreasing order, allowing adjacent equal values and leaving the input unchanged. This exercise covers verifying whole-range ordering.

# Solution

```cpp
return std::ranges::is_sorted(values);
```
