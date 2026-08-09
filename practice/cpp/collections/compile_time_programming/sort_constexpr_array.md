# Name

Sort an Array at Compile Time

# Description

Sort the supplied fixed array copy in ascending order and return it, with sorting performed during constant evaluation. This trains C++20 constant-evaluable ranges sorting rather than implementing a sorting algorithm.

# Solution

```cpp
std::ranges::sort(values);
return values;
```
