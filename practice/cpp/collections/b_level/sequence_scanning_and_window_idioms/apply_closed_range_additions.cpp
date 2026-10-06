#include <cstddef>
#include <vector>

using namespace std;

struct RangeAddition {
    std::size_t first;
    std::size_t last;
    long long delta;
};

std::vector<long long> apply_closed_range_additions(
    std::size_t size,
    const std::vector<RangeAddition>& updates) {
    // Pattern: difference array. Record each closed update at its start and immediately after its end, then materialize one running total.

    // Finish: return a vector of length size whose entries sum delta from all updates covering that index, or zero if none cover it; ranges include both zero-based endpoints and satisfy first <= last < size; size zero with no updates returns empty; preserve updates, size plus one fits in size_t, and all intermediate arithmetic fits in long long
}
