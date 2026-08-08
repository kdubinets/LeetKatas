# Name

Convert System Days to a Date

# Description

Recover the civil year, month, and day fields represented by a `std::chrono::sys_days` time point. This is the inverse calendar view of a day-precision system-clock value.

# Solution

```cpp
return std::chrono::year_month_day{value};
```
