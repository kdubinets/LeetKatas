#include <cstddef>
#include <vector>

using namespace std;

void collect_target_sum_combinations(
    const std::vector<int>& candidates,
    std::size_t start,
    int remaining,
    std::vector<int>& path,
    std::vector<std::vector<int>>& result) {
    // Pattern: sorted reusable-choice backtracking. Choose candidates from start onward, recurse with the same index and reduced remainder, restore the path, and stop the loop when a positive candidate exceeds the remainder.

    // Finish: append every nondecreasing completion of the supplied path whose added values sum to remaining, considering candidates from start and allowing reuse, and leave path unchanged on return; candidates is strictly increasing, positive, and not modified, and the initial call has start 0 with positive remaining and empty path and result
}

std::vector<std::vector<int>> target_sum_combinations(
    const std::vector<int>& candidates,
    int target) {
    std::vector<int> path;
    std::vector<std::vector<int>> result;
    collect_target_sum_combinations(candidates, 0, target, path, result);
    return result;
}
