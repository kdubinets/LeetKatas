#include <cstddef>
#include <vector>

struct RangeAddition {
    std::size_t first;
    std::size_t last;
    long long delta;
};

std::vector<long long> apply_closed_range_additions(
    std::size_t size,
    const std::vector<RangeAddition>& updates) {
    // Pattern: difference array. Record each closed update at its start and immediately after its end, then materialize one running total.
    // Finish: return size values after applying every update; every update is an in-bounds inclusive range
}
