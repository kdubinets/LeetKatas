#include <cstddef>
#include <vector>

using namespace std;

std::vector<std::vector<int>> unique_subsets_from_duplicates(
    const std::vector<int>& sorted_values) {
    // Pattern: emit-then-choose backtracking over sorted values. Emit each current path, skip equal candidates only at the same search depth, and restore the path after each branch.

    // Finish: return every distinct subset of sorted_values exactly once, with each subset nondecreasing and the subsets in lexicographic order, preserving the input; sorted_values is nondecreasing, each occurrence can be selected at most once, and empty input returns one empty subset
}
