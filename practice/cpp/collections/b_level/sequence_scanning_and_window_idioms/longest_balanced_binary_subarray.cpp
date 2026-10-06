#include <algorithm>
#include <algorithm>
#include <cstddef>
#include <unordered_map>
#include <vector>

using namespace std;

std::size_t longest_balanced_binary_subarray(const std::vector<int>& values) {
    // Pattern: first-occurrence prefix state. Treat zero and one as opposite balance changes, retaining the earliest prefix position for each balance.

    // Finish: return the longest nonempty contiguous range length with equally many 0s and 1s, or zero if none exists, including empty input; every value is 0 or 1, preserve values, and assume every prefix balance fits in long long
}
