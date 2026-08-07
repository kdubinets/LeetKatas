# Name

Shift a Bitset Window

# Description

Shift a copied `std::bitset<32>` toward higher-indexed positions by `count`, discard bits shifted beyond the fixed width, fill low positions with zeroes, and return it. Counts at least 32 produce an all-zero result. This exercise covers fixed-size bitset compound shifting.

# Solution

```cpp
bits <<= count;
return bits;
```
