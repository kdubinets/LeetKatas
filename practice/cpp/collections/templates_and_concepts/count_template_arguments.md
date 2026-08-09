# Name

Count Template Arguments

# Description

Return the number of types in the `Types` template parameter pack as `std::size_t`. The result must work in constant evaluation, including for an empty pack.

# Solution

```cpp
return sizeof...(Types);
```
