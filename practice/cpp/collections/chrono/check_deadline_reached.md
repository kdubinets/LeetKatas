# Name

Check a Deadline

# Description

Return whether a supplied monotonic-clock reading is at or after a deadline. Equality counts as reached, and no live clock query should be performed inside the function.

# Solution

```cpp
return now >= deadline;
```
