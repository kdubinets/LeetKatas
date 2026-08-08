# Name

Cast Time-Point Precision

# Description

Convert a system-clock time point to the same clock with millisecond precision, truncating any finer ticks toward zero in its duration since the epoch. This trains time-point conversion rather than duration-only conversion.

# Solution

```cpp
return std::chrono::time_point_cast<std::chrono::milliseconds>(value);
```
