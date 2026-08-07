# Name

Take a Fixed Span Suffix

# Description

Return a fixed-extent two-element span over the final elements of a read-only six-element span. The result must retain its size in its type. This exercise covers compile-time-sized span suffixes.

# Solution

```cpp
return values.last<2>();
```
