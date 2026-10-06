#include <cstddef>
#include <vector>

using namespace std;

std::vector<std::vector<int>> permute_distinct_values(const std::vector<int>& values) {
    // Pattern: position-choice backtracking. Scan input indices in order, choose an unused position, and restore both the path and its used marker after each branch; stop when every position is chosen.

    // Finish: return every permutation of values, ordered lexicographically by its sequence of original input indices, preserving the input; values are distinct, and empty input returns one empty permutation
}
