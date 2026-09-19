#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::vector<long long> range_sum_queries(
    const std::vector<int>& values,
    const std::vector<std::pair<std::size_t, std::size_t>>& queries) {
    // Pattern: one-past prefix sums. Each prefix position represents the total before that position, so an inclusive range is a difference of two prefixes.

    // Finish: return one sum per query, in query order; each pair {first, last} requests the sum of values from index first through last, including both endpoints; every range satisfies first <= last < values.size()
}
