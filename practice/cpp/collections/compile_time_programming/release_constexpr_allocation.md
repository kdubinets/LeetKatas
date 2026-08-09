# Name

Release a Constexpr Allocation

# Description

During constant evaluation, allocate a three-element integer array initialized to `2`, `3`, and `5`, compute its total, release the array, and return the total. C++20 permits temporary dynamic allocation only when its storage does not escape constant evaluation.

# Solution

```cpp
int* values = new int[3]{2, 3, 5};
const int total = values[0] + values[1] + values[2];
delete[] values;
return total;
```
