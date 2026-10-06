#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long maximum_capacity_value(
    const std::vector<std::size_t>& weights,
    const std::vector<int>& values,
    std::size_t capacity) {
    // Pattern: one capacity row for zero-one choices, initially all zero. For each item visit capacities from high to low; the new best at a capacity is the greater of its prior value and the prior best at capacity minus weight plus this item's value.

    // Finish: return the greatest total value of a subset whose total weight is at most capacity, selecting each item at most once; weights and values have equal length, weights are positive, and values are nonnegative; empty input or zero capacity returns zero; preserve both inputs, capacity plus one fits in size_t, and all total values fit in long long
}
