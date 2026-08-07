# Name

Replace a Bit Field

# Description

Replace `width` bits in a `std::uint32_t` starting at the zero-based `offset`, using the lowest `width` bits of another value, while preserving every bit outside the field. The offset is below the type width and the field remains within the value; width may be zero or, at offset zero, the complete type width. This exercise covers clearing and inserting a bounded unsigned bit field safely.

# Solution

```cpp
auto low_mask = width == std::numeric_limits<std::uint32_t>::digits
    ? std::numeric_limits<std::uint32_t>::max()
    : (std::uint32_t{1} << width) - 1;
auto field_mask = low_mask << offset;
return (value & ~field_mask) | ((replacement & low_mask) << offset);
```
