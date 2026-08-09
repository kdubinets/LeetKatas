# Name

Bring Enumerators into Scope

# Description

Inside `is_active`, bring all enumerators from scoped enum `Status` into the function scope with the C++20 enum using-declaration, then compare `status` with the unqualified `running` name.

# Solution

```cpp
using enum Status;
return status == running;
```
