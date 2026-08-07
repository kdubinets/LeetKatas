# Name

Make a Unique Array

# Description

Return an exclusively owned runtime-sized array of `count` integers, with every element value-initialized to zero. This exercise covers safe construction of a dynamic array with `std::unique_ptr<int[]>`.

# Solution

```cpp
return std::make_unique<int[]>(count);
```
