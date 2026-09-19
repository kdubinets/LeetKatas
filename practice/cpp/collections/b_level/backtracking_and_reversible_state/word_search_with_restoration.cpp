#include <cstddef>
#include <string>
#include <string_view>
#include <vector>

using namespace std;

bool word_exists_from(
    std::vector<std::string>& grid,
    long long row,
    long long column,
    std::string_view word,
    std::size_t index) {
    // Pattern: temporary grid marking. After matching the current byte, replace the cell with a non-lowercase marker, explore four neighbors, then restore the byte before every return.

    // Finish: return whether word[index:] can be matched from this cell through horizontal or vertical neighbors without reusing a cell; grid is rectangular lowercase text, word is lowercase and index is valid, out-of-bounds or mismatched cells return false, and grid must be exactly restored
}

bool word_exists(std::vector<std::string>& grid, std::string_view word) {
    if (word.empty()) {
        return true;
    }
    for (std::size_t row = 0; row < grid.size(); ++row) {
        for (std::size_t column = 0; column < grid[row].size(); ++column) {
            if (word_exists_from(grid, row, column, word, 0)) {
                return true;
            }
        }
    }
    return false;
}
