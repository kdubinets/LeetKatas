# Name

Ceil a Duration

# Description

Round a millisecond duration upward to the least whole-second duration not less than it. The behavior must remain correct for both positive and negative inputs.

# Solution

```cpp
return std::chrono::ceil<std::chrono::seconds>(value);
```
