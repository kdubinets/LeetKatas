# Name

Find the Last Day of a Month

# Description

Given a valid `std::chrono::year_month`, return its final numbered `std::chrono::day`. The result must account for varying month lengths and leap years.

# Solution

```cpp
return (value / std::chrono::last).day();
```
