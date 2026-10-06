#include <algorithm>
#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

long long minimum_step_cost_from(std::size_t index, const std::vector<int>& costs) {
    // Pattern: top-down memoization. At or beyond the end the cost is zero; otherwise add the current cost to the smaller result from advancing one or two positions. Begin with uncomputed cache entries and distinguish them from computed results, including zero.

    // Finish: return the minimum total cost from index until reaching or passing costs.size(), paying costs at every visited in-range index including the starting index and advancing one or two positions per move; return zero if index is already at or beyond the end; costs may be negative, preserve costs, and all totals fit in long long
}
