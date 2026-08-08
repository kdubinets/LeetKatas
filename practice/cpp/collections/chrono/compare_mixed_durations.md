# Name

Compare Mixed Durations

# Description

Return whether an integral seconds duration is strictly shorter than an integral milliseconds duration. Compare the typed durations directly without extracting counts or manually scaling either value.

# Solution

```cpp
return left < right;
```
