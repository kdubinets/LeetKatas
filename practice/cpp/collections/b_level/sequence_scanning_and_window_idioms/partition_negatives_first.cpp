#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::size_t partition_negatives_first(std::vector<int>& values) {
    // Pattern: opposing partition pointers. Values before the left boundary are negative and values at or after the right boundary are nonnegative.

    // Finish: rearrange values in place so negatives precede nonnegative values; return the first nonnegative index, or values.size() if none exists; either group's order may change, preserve size and every value's multiplicity, and empty input returns zero
}
