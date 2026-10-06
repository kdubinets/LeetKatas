# Name

Grid Word Search with Restored Cells

# Description

Return whether the word can be formed from any starting cell in a rectangular grid of lowercase text, moving horizontally or vertically without reusing a cell. The word is lowercase. An empty word is found, while a nonempty word cannot be found in an empty grid. Restore the grid exactly on both success and failure.

Use temporary grid marking, exploring neighbors of matched cells and restoring each marked cell before returning. The learner implements the complete function, including traversal from all starting cells and its recursive state.

This exercise covers restoration of temporarily mutated search state on every return path.

# Solution

```cpp
if (word.empty()) {
    return true;
}
auto search = [&](auto&& self, long long row, long long column,
                  std::size_t index) -> bool {
    if (row < 0 || column < 0 ||
        row >= static_cast<long long>(grid.size()) ||
        column >= static_cast<long long>(grid[row].size()) ||
        grid[row][column] != word[index]) {
        return false;
    }
    const char saved = grid[row][column];
    grid[row][column] = '\0';
    bool found = index + 1 == word.size();
    if (!found) {
        const long long offsets[5] = {-1, 0, 1, 0, -1};
        for (int direction = 0; direction < 4 && !found; ++direction) {
            found = self(self, row + offsets[direction],
                         column + offsets[direction + 1], index + 1);
        }
    }
    grid[row][column] = saved;
    return found;
};
for (std::size_t row = 0; row < grid.size(); ++row) {
    for (std::size_t column = 0; column < grid[row].size(); ++column) {
        if (search(search, row, column, 0)) {
            return true;
        }
    }
}
return false;
```
