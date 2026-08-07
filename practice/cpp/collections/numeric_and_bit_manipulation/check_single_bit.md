# Name

Check for a Single Set Bit

# Description

Return whether an `unsigned int` has exactly one set bit. Zero must return false. This exercise covers the C++20 power-of-two bit query without manual subtraction or masking tricks.

# Solution

```cpp
return std::has_single_bit(value);
```
