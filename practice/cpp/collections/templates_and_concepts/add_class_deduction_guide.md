# Name

Add a Class Deduction Guide

# Description

Add a deduction guide for `Holder` so construction from `const char*` deduces `Holder<std::string>`. This gives the holder ownership instead of storing the pointer type.

# Solution

```cpp
Holder(const char*) -> Holder<std::string>;
```
