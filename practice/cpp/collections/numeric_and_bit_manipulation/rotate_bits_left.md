# Name

Rotate Bits to the Left

# Description

Circularly rotate a `std::uint32_t` left by an `int` distance and return the result. Distances outside the bit width, including negative distances, use the standard normalized rotation behavior. This exercise covers C++20 bit rotation without undefined shifts.

# Solution

```cpp
return std::rotl(value, distance);
```
