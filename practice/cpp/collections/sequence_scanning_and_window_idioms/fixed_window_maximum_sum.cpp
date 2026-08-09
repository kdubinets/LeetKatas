#include <algorithm>
#include <cstddef>
#include <vector>

long long maximum_window_sum(const std::vector<int>& values, std::size_t width) {
    if (width == 0 || width > values.size()) {
        return 0;
    }

    // Pattern: fixed-size rolling window. Update the total by adding the entering value and removing the leaving value.
    // Finish: return the greatest sum of any contiguous window of width values
}
