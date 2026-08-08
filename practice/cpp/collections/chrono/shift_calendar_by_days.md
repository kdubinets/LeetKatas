# Name

Shift a Calendar Date by Days

# Description

Move a valid civil date forward or backward by an exact signed day count and return the resulting civil date. Perform the arithmetic on the continuous day timeline so month and year boundaries are handled correctly.

# Solution

```cpp
return std::chrono::year_month_day{
    std::chrono::sys_days{date} + offset};
```
