# Name

Find the Difference Between Year-Month Values

# Description

Return the signed `std::chrono::months` distance from one valid `year_month` value to another. Use calendar-month arithmetic so crossing a year boundary is handled directly.

# Solution

```cpp
return last - first;
```
