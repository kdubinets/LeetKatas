#include <cstddef>
#include <vector>

using namespace std;

void collect_unique_subsets(
    const std::vector<int>& sorted_values,
    std::size_t start,
    std::vector<int>& path,
    std::vector<std::vector<int>>& result) {
    // Pattern: emit-then-choose backtracking over sorted values. Emit the current path, and at each depth skip a value equal to the preceding candidate at that same depth; append, recurse, and restore otherwise.

    // Finish: append the supplied path and every distinct extension using indices from start in depth-first lexicographic order, and leave path unchanged on return; sorted_values is nondecreasing and not modified, the initial path and result are empty with start 0, and empty input appends one empty subset
}

std::vector<std::vector<int>> unique_subsets_from_duplicates(
    const std::vector<int>& sorted_values) {
    std::vector<int> path;
    std::vector<std::vector<int>> result;
    collect_unique_subsets(sorted_values, 0, path, result);
    return result;
}
