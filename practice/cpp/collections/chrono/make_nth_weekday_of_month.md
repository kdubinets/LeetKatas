# Name

Make an Nth Weekday of a Month

# Description

Construct a `std::chrono::year_month_weekday` representing occurrence `index` of a weekday in the supplied year and month. The index is in the calendar API's valid range of 1 through 5; the result itself can report whether that occurrence exists.

# Solution

```cpp
return value.year()
    / value.month()
    / std::chrono::weekday_indexed{weekday, index};
```
