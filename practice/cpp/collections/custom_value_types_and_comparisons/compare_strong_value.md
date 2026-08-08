# Name

Compare a Strongly Ordered Value

# Description

Implement the three-way comparison for an integer-backed revision value. The result must preserve the integer field's strong ordering category.

# Solution

```cpp
return left.value <=> right.value;
```
