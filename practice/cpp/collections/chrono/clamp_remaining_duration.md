# Name

Clamp Remaining Duration

# Description

Return the millisecond duration remaining from `now` until `deadline`. If the deadline has arrived or passed, return a zero duration rather than a negative value.

# Solution

```cpp
return deadline > now
    ? deadline - now
    : std::chrono::milliseconds::zero();
```
