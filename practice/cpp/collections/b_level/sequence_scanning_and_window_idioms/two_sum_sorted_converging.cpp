#include <cstddef>
#include <optional>
#include <utility>
#include <vector>

using namespace std;

std::optional<std::pair<std::size_t, std::size_t>> two_sum_sorted_indices(
    const std::vector<int>& values,
    long long target) {
    // Pattern: converging two pointers on sorted input. Move one endpoint according to whether its pair sum is too small or too large.

    // Finish: return any pair of distinct zero-based indices whose values sum to target, or an empty optional if no such pair exists; values are sorted in nondecreasing order and may contain duplicates
}
