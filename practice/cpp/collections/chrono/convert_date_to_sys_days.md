# Name

Convert a Date to System Days

# Description

Convert a valid civil `year_month_day` into the corresponding day-precision system-clock time point. The date is guaranteed valid before conversion.

# Solution

```cpp
return std::chrono::sys_days{date};
```
