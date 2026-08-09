# Name

Validate with Static Assert

# Description

Add a compile-time assertion that the integer port `443` satisfies the supplied constant-evaluable validity function. This trains enforcing a computed invariant during translation without adding runtime code.

# Solution

```cpp
static_assert(valid_port(443));
```
