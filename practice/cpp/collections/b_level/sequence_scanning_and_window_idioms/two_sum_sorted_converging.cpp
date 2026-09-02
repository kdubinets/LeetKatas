#include <cstddef>
#include <optional>
#include <utility>
#include <vector>

std::optional<std::pair<std::size_t, std::size_t>> two_sum_sorted_indices(
    const std::vector<int>& values,
    long long target) {
    // Pattern: converging two pointers on sorted input. Move one endpoint according to whether its pair sum is too small or too large.
    // Finish: return indices of two values whose sum is target, or no result when no pair exists
}
