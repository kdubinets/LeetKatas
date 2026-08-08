# Name

Collect Mutable References

# Description

Return a vector containing mutable reference wrappers for every element of the input vector in order. Changes made through the result must affect the original integers, whose lifetime is guaranteed to outlast the wrappers.

# Solution

```cpp
return std::vector<std::reference_wrapper<int>>(
    values.begin(), values.end());
```
