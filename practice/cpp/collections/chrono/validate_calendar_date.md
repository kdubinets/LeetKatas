# Name

Validate a Calendar Date

# Description

Return whether a `std::chrono::year_month_day` has valid year, month, and day fields as a complete civil date. The check must account for month length and leap years.

# Solution

```cpp
return date.ok();
```
