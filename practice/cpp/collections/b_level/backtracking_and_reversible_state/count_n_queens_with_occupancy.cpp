#include <cstddef>
#include <vector>

using namespace std;

std::size_t count_n_queens(std::size_t size) {
    // Pattern: one queen per row with reversible occupancy. Track occupied columns and both diagonal families (row+column and row+size-column-1); restore all three marks after each branch and count a placement when every row is filled.

    // Finish: return the number of ways to place size queens on a size-by-size board so that no two share a row, column, or diagonal; size is positive
}
