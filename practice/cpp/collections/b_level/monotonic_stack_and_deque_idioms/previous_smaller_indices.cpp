#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

std::vector<std::optional<std::size_t>> previous_smaller_indices(const std::vector<int>& values) {
    // Pattern: increasing stack of candidate indices. Remove candidates whose values are greater than or equal to the current value; the remaining top is the nearest strict boundary.

    // Finish: return one entry per position containing the nearest earlier index with a strictly smaller value, or an empty optional when none exists; return an empty vector for empty input and do not modify values
}
