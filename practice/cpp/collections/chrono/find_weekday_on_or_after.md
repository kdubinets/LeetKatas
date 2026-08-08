# Name

Find a Weekday On or After a Date

# Description

Given a valid civil date and valid weekday, return the first date on or after the input that has the requested weekday. Return the original date when it already falls on that weekday.

# Solution

```cpp
const std::chrono::sys_days current{date};
return std::chrono::year_month_day{
    current + (requested - std::chrono::weekday{current})};
```
