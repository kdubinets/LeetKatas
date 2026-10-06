# Name

Count N-Queens with Coupled Occupancy

# Description

For a positive board size, return the number of ways to place that many queens on the square board with no shared row, column, or diagonal.

Use one-queen-per-row backtracking with reversible column and diagonal occupancy. Diagonal indices are row+column and row+size-column-1. Restore all three occupancy marks after each branch and count a placement when all rows are filled. The learner implements the complete function, including its occupancy storage and recursive state.

This exercise covers reversible updates across multiple coupled constraint tables.

# Solution

```cpp
std::vector<bool> columns(size, false);
std::vector<bool> descending(2 * size - 1, false);
std::vector<bool> ascending(2 * size - 1, false);
auto search = [&](auto&& self, std::size_t row) -> std::size_t {
    if (row == size) {
        return 1;
    }
    std::size_t count = 0;
    for (std::size_t column = 0; column < size; ++column) {
        const std::size_t down = row + column;
        const std::size_t up = row + size - column - 1;
        if (columns[column] || descending[down] || ascending[up]) {
            continue;
        }
        columns[column] = descending[down] = ascending[up] = true;
        count += self(self, row + 1);
        columns[column] = descending[down] = ascending[up] = false;
    }
    return count;
};
return search(search, 0);
```
