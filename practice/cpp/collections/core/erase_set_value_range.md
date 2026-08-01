# Name

Erase Set Value Range

# Description

Remove every integer in the half-open value interval `[low, high)` from a mutable ordered set, where `low <= high`. Values outside that interval must remain. This exercise covers deriving and erasing an associative iterator range.

# Solution

```cpp
values.erase(values.lower_bound(low), values.lower_bound(high));
```
