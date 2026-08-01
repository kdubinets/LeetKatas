# Name

Make Ordered Set from Vector

# Description

Construct and return a `std::set<int>` from a const vector so duplicates are removed and iteration order is ascending, without modifying the input. This exercise covers associative-container range construction.

# Solution

```cpp
return {values.begin(), values.end()};
```
