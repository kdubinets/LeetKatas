# Name

Grid Word Search with Restored Cells

# Description

Return whether the remaining word can be matched from the supplied grid cell using four-neighbor moves without cell reuse. Grid and word are lowercase, index is valid, and out-of-range or mismatched cells fail. Restore the grid exactly on success and failure. The wrapper treats an empty word as found.

The supplied search temporarily replaces a matched cell with a non-lowercase marker, explores neighbors, and restores before returning.

This exercise covers restoration of temporarily mutated search state on every return path.

# Solution

```cpp
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
        found = word_exists_from(
            grid,
            row + offsets[direction],
            column + offsets[direction + 1],
            word,
            index + 1);
    }
}
grid[row][column] = saved;
return found;
```
