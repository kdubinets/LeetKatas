# Name

Check Vector Permutation

# Description

Return whether two const integer vectors contain the same values with the same multiplicities, regardless of order. Unequal lengths cannot match, and neither input may be modified. This exercise covers whole-range permutation comparison.

# Solution

```cpp
return std::ranges::is_permutation(left, right);
```
