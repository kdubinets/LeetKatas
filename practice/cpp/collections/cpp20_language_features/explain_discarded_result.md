# Name

Explain a Discarded Result

# Description

Apply the C++20 reason-bearing form of the `nodiscard` attribute to `check_status`. Its diagnostic message must be `"check the status"` when a caller discards the returned `Status`.

# Solution

```cpp
[[nodiscard("check the status")]]
```
