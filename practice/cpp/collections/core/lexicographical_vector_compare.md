# Name

Lexicographical Vector Compare

# Description

Return whether one const integer vector is lexicographically less than another: compare the first differing elements, with an exhausted proper prefix ordered first. This exercise covers conventional range-based lexicographical ordering.

# Solution

```cpp
return std::ranges::lexicographical_compare(left, right);
```
