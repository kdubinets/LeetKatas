# Name

Reject Invalid Immediate Input

# Description

Complete the immediate percentage validator so values in the inclusive range `0` through `100` are returned unchanged and any other call cannot produce a constant expression. The supplied valid call must continue to compile.

# Solution

```cpp
if (value < 0 || value > 100) {
    throw "percentage out of range";
}
return value;
```
