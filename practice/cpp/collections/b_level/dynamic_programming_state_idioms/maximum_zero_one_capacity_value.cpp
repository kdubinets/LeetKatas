#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long maximum_capacity_value(
    const std::vector<std::size_t>& weights,
    const std::vector<int>& values,
    std::size_t capacity) {
    // Pattern: one capacity row for zero-one choices. For each item, visit capacities from high to low so every transition reads state from before that item; best[c] = max(best[c], best[c - weight] + value).

    // Finish: return the greatest total value of a subset whose total weight is at most capacity; weights and values have equal length, every weight is positive, every value is nonnegative, and each item may be selected at most once; do not modify either input, and assume all total values fit in long long
}
