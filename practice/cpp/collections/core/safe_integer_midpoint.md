# Name

Safe Integer Midpoint

# Description

Return the integer midpoint of two arbitrary `int` values without overflow. When their mathematical midpoint lies exactly between two integers, choose the result closer to the first argument. This exercise covers C++20's overflow-safe midpoint utility.

# Solution

```cpp
return std::midpoint(left, right);
```
