# Name

Measure an Unsigned Value's Bit Width

# Description

Return the number of binary digits needed to represent an `unsigned int` without leading zeroes. The result for zero is zero. This exercise covers the C++20 bit-width query and makes its zero behavior explicit.

# Solution

```cpp
return static_cast<int>(std::bit_width(value));
```
