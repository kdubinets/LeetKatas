#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long minimum_falling_path_sum(const std::vector<std::vector<int>>& grid) {
    // Pattern: rotate separate previous and current rows. Initialize previous from the first row; each later cell adds its value to the minimum valid prior-row neighbor in the same or an adjacent column.

    // Finish: return the minimum sum from any first-row cell to any last-row cell, choosing in each next row the same or an adjacent column; grid is nonempty and rectangular with at least one column; do not modify grid, and assume every path sum fits in long long
}
