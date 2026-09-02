#include <cstddef>
#include <vector>

std::size_t first_not_less_index(const std::vector<int>& values, int target) {
    // Pattern: manual lower-bound search. The answer is always within the half-open interval, including the one-past-end insertion position.
    // Finish: return the first index whose ascending value is not less than target, or values.size() when none exists
}
