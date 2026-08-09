# Name

Select a Type Conditionally

# Description

Define alias template `selected_t` that resolves to `First` when `UseFirst` is true and `Second` otherwise. Use the supplied compile-time Boolean directly.

# Solution

```cpp
using selected_t = std::conditional_t<UseFirst, First, Second>;
```
