# Name

Count Leading Zero Bits

# Description

Return the number of consecutive zero bits at the most-significant end of a `std::uint32_t`. Zero has 32 leading zero bits. This exercise covers the C++20 leading-zero bit query and its defined zero behavior.

# Solution

```cpp
return std::countl_zero(value);
```
