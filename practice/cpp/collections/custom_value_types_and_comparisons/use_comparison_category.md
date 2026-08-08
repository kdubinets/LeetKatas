# Name

Interpret a Comparison Category

# Description

Given a `std::partial_ordering` result, return whether it represents the left operand being less than the right. Equivalent, greater, and unordered results must all return false.

# Solution

```cpp
return std::is_lt(order);
```
