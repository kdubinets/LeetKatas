#include <cstddef>
#include <vector>

using namespace std;

std::size_t first_not_less_index(const std::vector<int>& values, int target) {
    // Pattern: manual lower-bound search. Keep low <= answer <= high; values before low are less than target and values at or after high are not less than target.

    // Finish: return the first zero-based index i where values[i] >= target, or values.size() if none exists; values are sorted in nondecreasing order
}
