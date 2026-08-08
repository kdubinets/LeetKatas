# Name

Cast Duration Units

# Description

Convert an integral millisecond duration to whole seconds with truncation toward zero. The return type is `std::chrono::seconds`, making the potentially lossy conversion explicit.

# Solution

```cpp
return std::chrono::duration_cast<std::chrono::seconds>(value);
```
