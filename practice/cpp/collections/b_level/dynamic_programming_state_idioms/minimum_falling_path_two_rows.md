# Name

Minimum Falling Path with Two Rows

# Description

Return the minimum path sum from any first-row cell to any last-row cell, moving on each next row to the same or an adjacent column. The grid is nonempty, rectangular, and has at least one column. Do not modify it. Sums fit in long long.

The supplied recurrence rotates distinct previous and current rows; each current cell reads up to three prior-row neighbors.

This exercise covers rotation of separate rows with bounded prior-row dependencies.

# Solution

```cpp
std::vector<long long> previous(grid.front().begin(), grid.front().end());
std::vector<long long> current(previous.size());
for (std::size_t row = 1; row < grid.size(); ++row) {
    for (std::size_t column = 0; column < previous.size(); ++column) {
        long long best = previous[column];
        if (column > 0) best = std::min(best, previous[column - 1]);
        if (column + 1 < previous.size()) best = std::min(best, previous[column + 1]);
        current[column] = best + static_cast<long long>(grid[row][column]);
    }
    previous.swap(current);
}
return *std::min_element(previous.begin(), previous.end());
```
