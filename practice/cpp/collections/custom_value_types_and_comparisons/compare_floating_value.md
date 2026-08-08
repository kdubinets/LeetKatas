# Name

Preserve Floating-Point Partial Ordering

# Description

Implement three-way comparison for a double-backed measurement without converting unordered values such as NaN into an artificial total order. Preserve the field's comparison category.

# Solution

```cpp
return left.value <=> right.value;
```
