# Name

Disable an Indexed Bit Flag

# Description

Return a `std::uint32_t` with the zero-based bit at `position` cleared to zero while preserving all other bits. The caller guarantees that the position is in range. This exercise covers complementing a one-bit unsigned mask before applying it.

# Solution

```cpp
return flags & ~(std::uint32_t{1} << position);
```
