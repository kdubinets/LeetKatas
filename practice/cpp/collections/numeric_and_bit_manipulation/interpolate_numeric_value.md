# Name

Interpolate a Numeric Value

# Description

Return the linear interpolation from `start` to `end` at a `double` amount, where zero selects the start and one selects the end. Amounts outside that interval extrapolate. This exercise covers the standard interpolation utility and its endpoint-aware arithmetic behavior.

# Solution

```cpp
return std::lerp(start, end, amount);
```
