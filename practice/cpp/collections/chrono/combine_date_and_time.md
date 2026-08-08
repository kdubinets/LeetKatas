# Name

Combine a Date and Time

# Description

Combine a valid civil date with hour, minute, and second durations into a second-precision system-clock time point. The time fields are guaranteed to describe a time within that date: hours are 0–23, and minutes and seconds are 0–59.

# Solution

```cpp
return std::chrono::sys_days{date} + hour + minute + second;
```
