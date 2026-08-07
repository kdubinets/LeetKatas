# Name

Extract a Bit Field

# Description

Extract `width` bits from a `std::uint32_t`, starting at the zero-based `offset`, and return them shifted down to bit zero. The offset is below the type width and the requested field remains within the value; width may be zero or, when the offset is zero, the complete type width. This exercise covers safe shift-and-mask field extraction, including the full-width mask case.

# Solution

```cpp
auto mask = width == std::numeric_limits<std::uint32_t>::digits
    ? std::numeric_limits<std::uint32_t>::max()
    : (std::uint32_t{1} << width) - 1;
return (value >> offset) & mask;
```
