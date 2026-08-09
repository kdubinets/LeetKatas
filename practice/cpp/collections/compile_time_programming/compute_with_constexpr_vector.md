# Name

Compute with a Constexpr Vector

# Description

During constant evaluation, create an owning dynamic sequence containing `2` and `3`, append `5`, and return the sum of its elements. The vector is temporary and releases its allocation before evaluation completes. This trains C++20 constexpr `std::vector` operations.

# Solution

```cpp
std::vector<int> values{2, 3};
values.push_back(5);
return values[0] + values[1] + values[2];
```
