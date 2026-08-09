#include <cstddef>
#include <utility>
#include <vector>

std::vector<long long> range_sum_queries(
    const std::vector<int>& values,
    const std::vector<std::pair<std::size_t, std::size_t>>& queries) {
    // Pattern: one-past prefix sums. Each prefix position represents the total before that position, so an inclusive range is a difference of two prefixes.
    // Finish: return the sum for every inclusive query range; every query has valid first and second indices with first no greater than second
}
