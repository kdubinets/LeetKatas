# Name

Count N-Queens with Coupled Occupancy

# Description

Return the number of placements completing all remaining rows without shared columns or diagonals. Size is positive; wrapper state starts empty with correctly sized occupancy tables.

The supplied row-by-row search applies one queen to a column and both diagonal tables, recurses, and clears all three entries.

This exercise covers reversible updates across multiple coupled constraint tables.

# Solution

```cpp
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
    count += count_queen_placements(
        size, row + 1, columns, descending, ascending);
    columns[column] = descending[down] = ascending[up] = false;
}
return count;
```
