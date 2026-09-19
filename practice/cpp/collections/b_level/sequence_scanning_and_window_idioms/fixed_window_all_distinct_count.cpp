#include <cstddef>
#include <unordered_map>
#include <vector>

using namespace std;

std::size_t count_all_distinct_windows(const std::vector<int>& values, std::size_t width) {
    if (width == 0 || width > values.size()) {
        return 0;
    }

    // Pattern: fixed-size frequency window. Keep counts for precisely the values in the current window.

    // Finish: return the number of contiguous groups of exactly width elements in values with no repeated value; overlapping groups count separately
}
