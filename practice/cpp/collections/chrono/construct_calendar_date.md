# Name

Construct a Calendar Date

# Description

Construct and return a `std::chrono::year_month_day` from separate numeric year, month, and day fields. This exercise covers the strong calendar component types; validity is checked separately.

# Solution

```cpp
return std::chrono::year{year}
    / std::chrono::month{month}
    / std::chrono::day{day};
```
