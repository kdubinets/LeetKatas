# Name

Extract a Date from System Time

# Description

Return the civil `year_month_day` containing a system-clock time point. Round the time point downward to the day boundary before converting it, including for instants before the system-clock epoch.

# Solution

```cpp
return std::chrono::year_month_day{
    std::chrono::floor<std::chrono::days>(value)};
```
