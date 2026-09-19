#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long maximum_window_sum(const std::vector<int>& values, std::size_t width) {
    if (width == 0 || width > values.size()) {
        return 0;
    }

    // Pattern: fixed-size rolling window. Update the total by adding the entering value and removing the leaving value.

    // Finish: return the greatest sum among all contiguous groups of exactly width elements in values; the greatest sum may be negative
}
