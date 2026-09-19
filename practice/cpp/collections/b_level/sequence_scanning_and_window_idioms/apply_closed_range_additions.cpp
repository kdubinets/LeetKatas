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

    // Finish: return a vector of length size; each element equals the sum of delta from every update covering its index, or zero if none cover it; each range includes both first and last; indices are zero-based and every range satisfies first <= last < size
}
