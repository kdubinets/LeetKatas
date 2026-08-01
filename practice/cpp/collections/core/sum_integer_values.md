# Name

Sum Integer Values

# Description

Sum all integers in a const `std::vector<int>` and return a `long long`, ensuring accumulation is performed in the wider result type. This exercise covers typed numeric accumulation.

# Solution

```cpp
return std::accumulate(values.begin(), values.end(), 0LL);
```
