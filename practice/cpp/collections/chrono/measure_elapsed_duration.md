# Name

Measure Elapsed Duration

# Description

Subtract two monotonic-clock time points to return the signed duration from `start` to `finish`. A finish before the start must naturally produce a negative duration.

# Solution

```cpp
return finish - start;
```
