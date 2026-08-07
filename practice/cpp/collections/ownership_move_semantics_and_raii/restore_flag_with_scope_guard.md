# Name

Restore a Flag with a Scope Guard

# Description

After `active` is set true, install the supplied RAII guard and invoke the callable operation. The flag must become false on both normal return and exception unwinding. This exercise covers acquiring a scope guard before running work that may exit early.

# Solution

```cpp
FlagReset reset{active};
operation();
```
