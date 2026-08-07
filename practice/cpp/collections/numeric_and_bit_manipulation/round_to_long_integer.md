# Name

Round to a Long Integer

# Description

Round a finite `double` to the nearest `long`, with halfway cases rounded away from zero. The caller guarantees that the rounded result is representable. This exercise covers selecting a standard rounding operation whose return type and tie behavior match an explicit contract.

# Solution

```cpp
return std::lround(value);
```
