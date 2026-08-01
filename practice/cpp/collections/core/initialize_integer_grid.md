# Name

Initialize Integer Grid

# Description

Create and return a two-dimensional `std::vector<int>` with the requested `std::size_t` row and column counts, initializing every cell to the supplied integer. Zero dimensions must naturally produce the corresponding empty structure. This exercise covers nested vector construction.

# Solution

```cpp
return std::vector<std::vector<int>>(
    rows, std::vector<int>(columns, initial_value));
```
