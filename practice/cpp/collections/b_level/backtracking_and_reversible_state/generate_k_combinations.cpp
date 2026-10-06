#include <cstddef>
#include <vector>

using namespace std;

std::vector<std::vector<std::size_t>> generate_k_combinations(std::size_t n, std::size_t k) {
    // Pattern: increasing-choice backtracking. Keep the current path strictly increasing and restore it after each branch; stop at length k and prune when too few candidates remain.

    // Finish: return all combinations of k distinct values from 1 through n, with each combination strictly increasing and the combinations in lexicographic order; k <= n, and k == 0 returns one empty combination
}
