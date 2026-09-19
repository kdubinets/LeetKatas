#include <algorithm>
#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

long long minimum_step_cost_from(
    std::size_t index,
    const std::vector<int>& costs,
    std::vector<std::optional<long long>>& memo) {
    // Pattern: top-down memoization of the supplied recurrence. States at or beyond costs.size() cost zero; an in-range state is its cost plus the smaller result from advancing one or two positions, and an engaged optional caches even a zero result.

    // Finish: return the minimum total cost incurred from index to beyond the end when the cost at each visited in-range index is paid and each move advances one or two positions; costs may be negative, memo has costs.size() initially empty entries, and all totals fit in long long; return 0 when index is at or beyond the end and do not modify costs
}
