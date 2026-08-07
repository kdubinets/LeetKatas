# Name

Toggle an Indexed Bit Flag

# Description

Return a `std::uint32_t` with the zero-based bit at `position` reversed while preserving every other bit. The caller guarantees that the position is in range. This exercise covers toggling one flag with an unsigned exclusive-or mask.

# Solution

```cpp
return flags ^ (std::uint32_t{1} << position);
```
