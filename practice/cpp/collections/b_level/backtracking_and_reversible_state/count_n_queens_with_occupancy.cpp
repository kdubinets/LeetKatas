#include <cstddef>
#include <vector>

using namespace std;

std::size_t count_queen_placements(
    std::size_t size,
    std::size_t row,
    std::vector<bool>& columns,
    std::vector<bool>& descending,
    std::vector<bool>& ascending) {
    // Pattern: one queen per row with reversible occupancy. For each safe column, mark its column, row+column diagonal, and row+size-column-1 diagonal, recurse to the next row, then clear all three marks.

    // Finish: return the number of ways to place one queen in every row from row through size-1 without using an occupied column or diagonal, and leave all three occupancy vectors unchanged on return; size is positive, row <= size, the vectors have sizes size, 2*size-1, and 2*size-1 and describe queens in earlier rows, and the initial call has row 0 with every entry false
}

std::size_t count_n_queens(std::size_t size) {
    std::vector<bool> columns(size, false);
    std::vector<bool> descending(2 * size - 1, false);
    std::vector<bool> ascending(2 * size - 1, false);
    return count_queen_placements(
        size, 0, columns, descending, ascending);
}
