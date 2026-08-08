# Name

Round a Duration to Nearest

# Description

Round a millisecond duration to the nearest whole second. Exact halfway cases must follow the chrono rounding rule and select the result with an even count.

# Solution

```cpp
return std::chrono::round<std::chrono::seconds>(value);
```
