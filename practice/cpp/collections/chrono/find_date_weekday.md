# Name

Find a Date's Weekday

# Description

Return the `std::chrono::weekday` corresponding to a valid civil date. Convert through the day-precision system timeline so the weekday is derived from the complete date.

# Solution

```cpp
return std::chrono::weekday{std::chrono::sys_days{date}};
```
