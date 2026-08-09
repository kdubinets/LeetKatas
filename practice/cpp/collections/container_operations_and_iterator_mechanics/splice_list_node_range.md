# Name

Splice a List Node Range

# Description

Transfer the valid half-open node range `[first, last)` from `source` into `destination` immediately before `position`. Preserve node order and do not copy or move element values. The lists are distinct. This exercise covers the range form of `std::list` node transfer.

# Solution

```cpp
destination.splice(position, source, first, last);
```
