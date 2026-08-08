# Name

Make a Lexically Relative Path

# Description

Express `value` relative to `base` by comparing path components only. Neither path needs to exist, and an empty result is allowed when their root components are incompatible.

# Solution

```cpp
return value.lexically_relative(base);
```
