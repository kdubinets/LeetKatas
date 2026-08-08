# Name

Offset a Steady Time Point

# Description

Return the monotonic-clock time point reached by adding a millisecond delay to `start`. Inputs are guaranteed to keep the resulting time point representable.

# Solution

```cpp
return start + delay;
```
