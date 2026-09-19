#include <algorithm>
#include <cstddef>
#include <string>
#include <unordered_map>

using namespace std;

std::size_t longest_at_most_k_distinct_length(const std::string& text, std::size_t limit) {
    // Pattern: shrink-to-valid sliding window. Keep at most limit distinct bytes in the window by moving its left edge.

    // Finish: return the length of the longest contiguous substring of text containing at most limit different byte values; return zero when text is empty or limit is zero
}
