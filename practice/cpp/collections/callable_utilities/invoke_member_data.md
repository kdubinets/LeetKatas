# Name

Invoke a Data Member Pointer

# Description

Given a const `Record` and a pointer to either of its string data members, return a const reference to the selected member. This covers accessing member data through the same uniform invocation facility used for callables.

# Solution

```cpp
return std::invoke(member, record);
```
