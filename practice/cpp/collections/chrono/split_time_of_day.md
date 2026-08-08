# Name

Split a Time of Day

# Description

Convert a nonnegative millisecond duration since midnight into `std::chrono::hh_mm_ss<std::chrono::milliseconds>`, preserving hours, minutes, seconds, and subsecond milliseconds for field access.

# Solution

```cpp
return std::chrono::hh_mm_ss<std::chrono::milliseconds>{since_midnight};
```
