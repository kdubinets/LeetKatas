#include <cstddef>
#include <optional>
#include <utility>
#include <vector>

using namespace std;

std::optional<std::pair<std::size_t, std::size_t>> two_sum_sorted_indices(
    const std::vector<int>& values,
    long long target) {
    // Pattern: converging two pointers on sorted input. Move one endpoint according to whether its pair sum is too small or too large.

    // Finish: return any pair of distinct zero-based indices whose values sum to target, or an empty optional if no pair exists, including when fewer than two elements exist; values are nondecreasing, may contain duplicates, and must be preserved
}
