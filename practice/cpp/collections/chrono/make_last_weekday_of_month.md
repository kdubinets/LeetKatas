# Name

Make the Last Weekday of a Month

# Description

Construct a `std::chrono::year_month_weekday_last` representing the final occurrence of the supplied valid weekday within a valid year and month.

# Solution

```cpp
return value.year()
    / value.month()
    / std::chrono::weekday_last{weekday};
```
