# Name

Convert time_t to System Time

# Description

Convert a platform `std::time_t` value into `std::chrono::system_clock::time_point` using the system clock's defined boundary operation.

# Solution

```cpp
return std::chrono::system_clock::from_time_t(value);
```
