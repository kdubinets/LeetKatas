# Name

Check an Indexed Bit Flag

# Description

Return whether the zero-based bit at `position` is set in a `std::uint32_t` without changing the flags. The caller guarantees that the position is in range. This exercise covers constructing and testing a one-bit unsigned flag mask.

# Solution

```cpp
return (flags & (std::uint32_t{1} << position)) != 0;
```
