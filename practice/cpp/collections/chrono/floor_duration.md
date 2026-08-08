# Name

Floor a Duration

# Description

Round a millisecond duration downward to the greatest whole-second duration not exceeding it. This differs from truncation for negative fractional-second values.

# Solution

```cpp
return std::chrono::floor<std::chrono::seconds>(value);
```
