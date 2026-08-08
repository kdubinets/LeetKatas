# Name

Take a Duration's Magnitude

# Description

Return the absolute magnitude of a signed millisecond duration, preserving its duration type. Inputs are guaranteed not to contain the minimum representable count, whose positive magnitude would overflow.

# Solution

```cpp
return std::chrono::abs(value);
```
