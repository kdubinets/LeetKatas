# Name

Write an Abbreviated Function Template

# Description

Define `increment` with one abbreviated, integral-constrained by-value parameter. Return the result of adding one; normal integral promotion rules apply to the expression.

# Solution

```cpp
auto increment(std::integral auto value) {
    return value + 1;
}
```
