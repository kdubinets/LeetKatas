# Name

Round Down to a Power of Two

# Description

Return the greatest power of two not exceeding an `unsigned int`. Return zero when the input is zero. This exercise covers the C++20 bit-floor operation.

# Solution

```cpp
return std::bit_floor(value);
```
