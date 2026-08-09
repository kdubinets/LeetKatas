#include <algorithm>
#include <cstddef>
#include <unordered_map>
#include <vector>

std::size_t longest_balanced_binary_subarray(const std::vector<int>& values) {
    // Pattern: first-occurrence prefix state. Treat zero and one as opposite balance changes, retaining the earliest prefix position for each balance.
    // Finish: return the greatest length of a contiguous range with equally many zeroes and ones; values contain only zero or one
}
