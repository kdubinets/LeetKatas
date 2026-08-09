# Name

Add an Optional Variadic Comma

# Description

Define variadic macro `COMBINE(first, ...)` to call `combine`. Use C++20 conditional variadic replacement so a comma is emitted before the variadic arguments only when at least one is supplied.

# Solution

```cpp
#define COMBINE(first, ...) combine(first __VA_OPT__(,) __VA_ARGS__)
```
