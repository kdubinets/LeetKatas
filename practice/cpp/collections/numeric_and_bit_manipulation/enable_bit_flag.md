# Name

Enable an Indexed Bit Flag

# Description

Return a `std::uint32_t` with the zero-based bit at `position` set to one while preserving all other bits. The caller guarantees that the position is in range. This exercise covers construction and application of a one-bit unsigned flag mask.

# Solution

```cpp
return flags | (std::uint32_t{1} << position);
```
