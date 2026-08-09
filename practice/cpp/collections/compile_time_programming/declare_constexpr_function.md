# Name

Declare a Constexpr Function

# Description

Define `square` as an integer function whose result can be evaluated at compile time. It must return the mathematical square for positive and negative inputs. This trains the basic declaration and definition of a constant-evaluable function.

# Solution

```cpp
constexpr int square(int value) {
    return value * value;
}
```
