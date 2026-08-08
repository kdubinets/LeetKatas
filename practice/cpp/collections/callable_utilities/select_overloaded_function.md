# Name

Select an Overloaded Function

# Description

Return a `std::function<int(int)>` containing the integer overload of `convert`, rather than its double overload. Resolve the overloaded function name to the exact requested function-pointer signature before it is stored.

# Solution

```cpp
return static_cast<int (*)(int)>(&convert);
```
