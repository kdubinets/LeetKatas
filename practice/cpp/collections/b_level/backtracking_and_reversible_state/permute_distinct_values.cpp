#include <cstddef>
#include <vector>

using namespace std;

void collect_distinct_permutations(
    const std::vector<int>& values,
    std::vector<bool>& used,
    std::vector<int>& path,
    std::vector<std::vector<int>>& result) {
    // Pattern: position-choice backtracking. Scan input indices in order, mark one unused index, append its value, recurse, then remove the value and clear exactly that marker.

    // Finish: append to result every completion of the supplied path to a permutation in input-index choice order, treating true used markers as already chosen, and leave path and used unchanged on return; values is distinct and not modified, the initial call has all markers false and empty path and result, and empty input appends one empty permutation
}

std::vector<std::vector<int>> permute_distinct_values(const std::vector<int>& values) {
    std::vector<bool> used(values.size(), false);
    std::vector<int> path;
    std::vector<std::vector<int>> result;
    collect_distinct_permutations(values, used, path, result);
    return result;
}
