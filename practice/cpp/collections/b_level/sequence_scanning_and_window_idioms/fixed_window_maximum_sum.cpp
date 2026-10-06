#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long maximum_window_sum(const std::vector<int>& values, std::size_t width) {
    // Pattern: fixed-size rolling window. Update the total by adding the entering value and removing the leaving value.

    // Finish: return the greatest sum of any contiguous group of exactly width elements, which may be negative; return zero if width is zero or exceeds values.size(); preserve values and assume all intermediate sums fit in long long
}
