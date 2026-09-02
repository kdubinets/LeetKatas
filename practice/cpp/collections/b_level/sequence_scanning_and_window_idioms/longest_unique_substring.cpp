#include <array>
#include <algorithm>
#include <cstddef>
#include <string>

std::size_t longest_unique_substring_length(const std::string& text) {
    // Pattern: shrink-to-valid sliding window. Advance the left edge until every character occurs at most once.
    // Finish: return the greatest length of a substring with no repeated byte
}
