#include <cstddef>
#include <vector>

using namespace std;

void collect_k_combinations(
    std::size_t n,
    std::size_t k,
    std::size_t next,
    std::vector<std::size_t>& path,
    std::vector<std::vector<std::size_t>>& result) {
    // Pattern: increasing-choice backtracking. Append one candidate, recurse from its successor, then remove it; stop when path has k values and prune when too few candidates remain.

    // Finish: append to result every lexicographically ordered completion of the supplied increasing path to length k using values from next through n, and leave path unchanged on return; 0 <= k <= n, the initial call has next 1 with empty path and result, and k == 0 appends one empty combination
}

std::vector<std::vector<std::size_t>> generate_k_combinations(std::size_t n, std::size_t k) {
    std::vector<std::vector<std::size_t>> result;
    std::vector<std::size_t> path;
    collect_k_combinations(n, k, 1, path, result);
    return result;
}
