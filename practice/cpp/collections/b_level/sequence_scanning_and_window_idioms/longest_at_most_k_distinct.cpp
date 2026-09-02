#include <algorithm>
#include <cstddef>
#include <string>
#include <unordered_map>

std::size_t longest_at_most_k_distinct_length(const std::string& text, std::size_t limit) {
    // Pattern: shrink-to-valid sliding window. Keep at most limit distinct bytes in the window by moving its left edge.
    // Finish: return the greatest substring length with at most limit distinct bytes
}
