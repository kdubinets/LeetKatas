#include <cstddef>
#include <vector>

using namespace std;

std::vector<std::vector<int>> target_sum_combinations(
    const std::vector<int>& candidates,
    int target) {
    // Pattern: sorted reusable-choice backtracking. Keep choices nondecreasing, allow the selected candidate again, and restore the path after each branch; emit at zero remainder and stop considering candidates once they exceed the remainder.

    // Finish: return every distinct nondecreasing combination of candidates summing to target, allowing each candidate to be reused any number of times and preserving the input; candidates are strictly increasing and positive, target is positive, and no solution returns an empty result
}
