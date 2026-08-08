# Name

Adapt a Member Function

# Description

Return a `std::function<int(const Scale&, int)>` backed by the `Scale::apply` member function. The resulting callable must accept an object as its first argument and the member function's integer argument as its second.

# Solution

```cpp
return std::mem_fn(&Scale::apply);
```
