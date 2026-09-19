#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

std::vector<std::optional<std::size_t>> next_greater_indices(const std::vector<int>& values) {
    // Pattern: decreasing stack of unresolved indices. Resolve from the top while the arriving value is strictly greater; equal values remain unresolved.

    // Finish: return one entry per input position containing the nearest later index with a strictly greater value, or an empty optional when none exists; return an empty vector for empty input and do not modify values
}
