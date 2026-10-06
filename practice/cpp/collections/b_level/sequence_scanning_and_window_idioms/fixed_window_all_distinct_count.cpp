#include <cstddef>
#include <unordered_map>
#include <vector>

using namespace std;

std::size_t count_all_distinct_windows(const std::vector<int>& values, std::size_t width) {
    // Pattern: fixed-size frequency window. Keep counts for precisely the values in the current window.

    // Finish: return the number of contiguous groups of exactly width elements with no repeated value, counting overlapping groups separately; return zero if width is zero or exceeds values.size(), and preserve values
}
