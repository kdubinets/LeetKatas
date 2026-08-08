# Name

Make a Same-Type Pair Callable

# Description

Return a C++20 template lambda whose two by-value parameters share one explicitly declared template type and whose result is `std::pair<T, T>`. Transfer the parameter values into the result so movable types do not require an additional copy. This trains explicit template parameter lists on lambdas rather than independent `auto` deduction.

# Solution

```cpp
return []<typename T>(T first, T second) {
    return std::pair<T, T>{std::move(first), std::move(second)};
};
```
