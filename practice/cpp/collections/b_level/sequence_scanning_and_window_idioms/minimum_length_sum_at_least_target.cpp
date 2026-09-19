#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

std::size_t minimum_length_sum_at_least_target(
    const std::vector<int>& positive_values,
    long long target) {
    // Pattern: shrink-to-valid sliding window. With positive values and a positive target, remove from the left while the current sum still meets the target.

    // Finish: return the length of the shortest nonempty contiguous range in positive_values whose elements sum to at least target, or zero if none exists; every input value and target are strictly positive
}
