#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

std::optional<std::size_t> binary_search_exact_index(const std::vector<int>& values, int target) {
    // Pattern: manual binary search with a half-open candidate interval. Every possible matching index remains between low inclusive and high exclusive.

    // Finish: return any zero-based index i where values[i] equals target, or an empty optional if none exists; values are sorted in nondecreasing order
}
