#include <cstddef>
#include <vector>

using namespace std;

long long count_grid_paths(std::size_t rows, std::size_t columns) {
    // Pattern: one rolling row. The first cell starts at one; each other cell becomes prior-row ways already stored there plus current-row ways immediately to its left.

    // Finish: return the number of paths from the top-left to the bottom-right of a rows-by-columns grid when each move goes one cell right or down; rows and columns are positive, and every path count fits in long long
}
