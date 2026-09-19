# Name

Nearest Source Distances from Multiple Sources

# Description

Return each cell's fewest four-direction moves to any cell containing one. If there is no source, every result is empty. The grid is nonempty, rectangular, and preserved.

The supplied multi-source traversal enqueues all distance-zero sources before expansion and marks neighbors at enqueue time.

This exercise covers simultaneous initialization and expansion of a multi-source BFS frontier.

# Solution

```cpp
const std::size_t rows = grid.size();
const std::size_t columns = grid.front().size();
std::vector<std::vector<std::optional<std::size_t>>> distance(
    rows, std::vector<std::optional<std::size_t>>(columns));
std::queue<std::pair<std::size_t, std::size_t>> pending;
for (std::size_t row = 0; row < rows; ++row) {
    for (std::size_t column = 0; column < columns; ++column) {
        if (grid[row][column] == 1) {
            distance[row][column] = 0;
            pending.emplace(row, column);
        }
    }
}
const int offsets[5] = {-1, 0, 1, 0, -1};
while (!pending.empty()) {
    const auto [row, column] = pending.front();
    pending.pop();
    for (int direction = 0; direction < 4; ++direction) {
        const long long next_row = static_cast<long long>(row) + offsets[direction];
        const long long next_column = static_cast<long long>(column) + offsets[direction + 1];
        if (next_row >= 0 && next_column >= 0 &&
            next_row < static_cast<long long>(rows) &&
            next_column < static_cast<long long>(columns) &&
            !distance[next_row][next_column]) {
            distance[next_row][next_column] = *distance[row][column] + 1;
            pending.emplace(next_row, next_column);
        }
    }
}
return distance;
```
