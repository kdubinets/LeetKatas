# Name

Move a Member Out

# Description

Return the string stored in a mutable `Box` by moving its contents into the result. The member remains a valid string with unspecified contents. This exercise covers explicitly transferring from an lvalue member.

# Solution

```cpp
return std::move(box.value);
```
