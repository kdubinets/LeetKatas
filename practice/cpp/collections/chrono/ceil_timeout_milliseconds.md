# Name

Ceil a Timeout to Milliseconds

# Description

Convert a positive monotonic-clock duration to integral milliseconds for a timeout API. Any positive fractional millisecond must round upward so the converted timeout is never shorter than the requested remaining time.

# Solution

```cpp
return std::chrono::ceil<std::chrono::milliseconds>(remaining);
```
