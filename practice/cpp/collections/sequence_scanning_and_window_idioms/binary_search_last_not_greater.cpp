#include <cstddef>
#include <optional>
#include <vector>

std::optional<std::size_t> last_not_greater_index(const std::vector<int>& values, int target) {
    // Pattern: manual upper-bound search. Find the one-past-last acceptable position with a half-open interval before converting it to an index.
    // Finish: return the last index whose ascending value is not greater than target, or no result when every value is greater
}
