# Name

Count Grid Paths with One Rolling Row

# Description

Return the number of paths from the top-left to the bottom-right of a rows-by-columns grid when every move goes one cell right or one cell down. Both dimensions are positive, and all path counts fit in long long.

The supplied dynamic-programming model uses one rolling row. Its first cell starts at one; every other cell combines the prior-row value still stored at that column with the current-row value immediately to its left.

This exercise covers one-row in-place evaluation of supplied grid dependencies.

# Solution

```cpp
std::vector<long long> ways(columns, 0);
ways[0] = 1;
for (std::size_t row = 0; row < rows; ++row) {
    for (std::size_t column = 1; column < columns; ++column) {
        ways[column] += ways[column - 1];
    }
}
return ways.back();
```
