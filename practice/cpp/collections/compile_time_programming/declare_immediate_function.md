# Name

Declare an Immediate Function

# Description

Define `cube` as an integer function whose potentially evaluated calls are required to occur during constant evaluation. It must return the mathematical cube of its argument. This trains a C++20 immediate function rather than a merely constant-evaluable one.

# Solution

```cpp
consteval int cube(int value) {
    return value * value * value;
}
```
