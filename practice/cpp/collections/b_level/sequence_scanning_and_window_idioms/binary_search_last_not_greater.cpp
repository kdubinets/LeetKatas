#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

std::optional<std::size_t> last_not_greater_index(const std::vector<int>& values, int target) {
    // Pattern: manual upper-bound search. Find the one-past-last acceptable position with a half-open interval before converting it to an index.

    // Finish: return the last zero-based index i where values[i] <= target, or an empty optional if none exists, including for empty input; values are sorted in nondecreasing order
}
