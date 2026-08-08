# Name

Find the Difference Between Calendar Dates

# Description

Return the signed `std::chrono::days` distance from one valid civil date to another. Convert both dates to the continuous day-precision system timeline before subtracting them so month and year boundaries require no manual handling.

# Solution

```cpp
return std::chrono::sys_days{last} - std::chrono::sys_days{first};
```
