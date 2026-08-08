# Name

Rebind a Reference Wrapper

# Description

Change a mutable `std::reference_wrapper<int>` so subsequent access through it refers to `replacement`. The integer previously referenced must not be assigned or modified.

# Solution

```cpp
target = std::ref(replacement);
```
