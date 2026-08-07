# Name

Round Up to a Power of Two

# Description

Return the smallest power of two not less than an `unsigned int`. The result for zero is one. The caller guarantees that the rounded result is representable in `unsigned int`. This exercise covers the C++20 bit-ceiling operation and its representability precondition.

# Solution

```cpp
return std::bit_ceil(value);
```
