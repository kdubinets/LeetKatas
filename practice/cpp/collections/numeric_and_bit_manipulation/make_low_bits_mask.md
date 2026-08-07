# Name

Make a Low-Bits Mask

# Description

Return a `std::uint32_t` whose lowest `count` bits are one and whose remaining bits are zero. The count is at most the type's bit width; zero produces zero and a full-width count produces all ones. This exercise covers safe unsigned mask construction without shifting by the type width.

# Solution

```cpp
if (count == std::numeric_limits<std::uint32_t>::digits) {
    return std::numeric_limits<std::uint32_t>::max();
}
return (std::uint32_t{1} << count) - 1;
```
