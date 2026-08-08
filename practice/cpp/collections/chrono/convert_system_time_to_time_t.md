# Name

Convert System Time to time_t

# Description

Convert a `std::chrono::system_clock::time_point` to the platform's `std::time_t` representation using the clock's defined boundary operation. Any precision loss follows the standard-library implementation.

# Solution

```cpp
return std::chrono::system_clock::to_time_t(value);
```
