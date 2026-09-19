#include <array>
#include <algorithm>
#include <cstddef>
#include <string>

using namespace std;

std::size_t longest_unique_substring_length(const std::string& text) {
    // Pattern: shrink-to-valid sliding window. Advance the left edge until every character occurs at most once.

    // Finish: return the length of the longest contiguous substring of text in which every byte occurs at most once; return zero for empty text
}
