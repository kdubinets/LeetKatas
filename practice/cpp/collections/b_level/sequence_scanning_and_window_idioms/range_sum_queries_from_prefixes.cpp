#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::vector<long long> range_sum_queries(
    const std::vector<int>& values,
    const std::vector<std::pair<std::size_t, std::size_t>>& queries) {
    // Pattern: one-past prefix sums. Each prefix position represents the total before that position, so an inclusive range is a difference of two prefixes.

    // Finish: return one sum per query in query order; each pair {first, last} requests values from zero-based first through last inclusive and satisfies first <= last < values.size(); no queries returns empty; preserve both inputs and assume all prefix and range sums fit in long long
}
