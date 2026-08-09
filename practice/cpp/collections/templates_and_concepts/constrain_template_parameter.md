# Name

Constrain a Template Parameter

# Description

Define `square` using `Arithmetic` directly in the template parameter list. Take and return the constrained type by value.

# Solution

```cpp
template <Arithmetic T>
T square(T value) {
    return value * value;
}
```
