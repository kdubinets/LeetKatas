# Name

Compute a Duration Remainder

# Description

Return the millisecond remainder after removing as many complete positive second intervals as possible from a nonnegative elapsed duration. The result must preserve subsecond precision.

# Solution

```cpp
return elapsed % interval;
```
