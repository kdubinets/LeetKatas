# Name

Select a Fixed Span Subview

# Description

From a read-only eight-element span, return the three elements beginning at index two as `std::span<const int, 3>`. This exercise covers selecting a span subview with compile-time offset and extent.

# Solution

```cpp
return values.subspan<2, 3>();
```
