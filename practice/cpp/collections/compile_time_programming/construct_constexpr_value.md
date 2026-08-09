# Name

Construct a Constexpr Value

# Description

Define the two-argument `Point` constructor so it initializes both integer members directly and permits `Point` objects to be created during constant evaluation. The supplied accessors expose the stored coordinates.

# Solution

```cpp
constexpr Point(int x, int y) : x_(x), y_(y) {}
```
