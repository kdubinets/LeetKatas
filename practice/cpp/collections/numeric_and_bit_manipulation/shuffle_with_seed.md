# Name

Shuffle Values with a Seed

# Description

Pseudorandomly shuffle a by-value vector and return it, initializing a local standard Mersenne Twister engine from the supplied 32-bit seed. The result retains exactly the original elements, and the same implementation and seed produce the same order. This exercise covers supplying a uniform random bit generator to the standard shuffle algorithm.

# Solution

```cpp
std::mt19937 engine{seed};
std::shuffle(values.begin(), values.end(), engine);
return values;
```
