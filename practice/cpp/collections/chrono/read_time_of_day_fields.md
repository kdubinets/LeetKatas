# Name

Read Time-of-Day Fields

# Description

Return the hours, minutes, seconds, and millisecond subseconds stored in an `hh_mm_ss<std::chrono::milliseconds>` value. Preserve each field as its corresponding chrono duration in the returned `TimeFields` tuple.

# Solution

```cpp
return {
    value.hours(),
    value.minutes(),
    value.seconds(),
    value.subseconds()};
```
