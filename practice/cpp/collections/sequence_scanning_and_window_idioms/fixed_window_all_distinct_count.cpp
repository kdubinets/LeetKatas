#include <cstddef>
#include <unordered_map>
#include <vector>

std::size_t count_all_distinct_windows(const std::vector<int>& values, std::size_t width) {
    if (width == 0 || width > values.size()) {
        return 0;
    }

    // Pattern: fixed-size frequency window. Keep counts for precisely the values in the current window.
    // Finish: return how many contiguous windows of width values contain no repeated value
}
