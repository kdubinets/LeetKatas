#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::size_t partition_negatives_first(std::vector<int>& values) {
    // Pattern: opposing partition pointers. Values before the left boundary are negative and values at or after the right boundary are nonnegative.

    // Finish: rearrange values in place so all negative values precede all values >= 0; return the first nonnegative index, or values.size() if none exists; either group's order may change
}
