# Name

Count Trailing Zero Bits

# Description

Return the number of consecutive zero bits at the least-significant end of a `std::uint32_t`. Zero has 32 trailing zero bits. This exercise covers the C++20 trailing-zero bit query and its defined zero behavior.

# Solution

```cpp
return std::countr_zero(value);
```
