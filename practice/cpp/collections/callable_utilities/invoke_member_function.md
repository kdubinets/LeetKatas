# Name

Invoke a Member Function

# Description

Given a `Counter`, a pointer to one of its integer member functions, and an argument, invoke the selected member on that object and return its integer result. This trains uniform member-function invocation.

# Solution

```cpp
return std::invoke(operation, counter, amount);
```
