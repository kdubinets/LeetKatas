#include <cstddef>
#include <optional>
#include <vector>

std::optional<std::size_t> binary_search_exact_index(const std::vector<int>& values, int target) {
    // Pattern: manual binary search with a half-open candidate interval. Every possible matching index remains between low inclusive and high exclusive.
    // Finish: return the index of target in ascending values, or no result when target is absent
}
