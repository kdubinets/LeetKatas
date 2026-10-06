#include <algorithm>
#include <cstddef>
#include <string_view>
#include <vector>

using namespace std;

std::size_t longest_common_subsequence_length(
    std::string_view first,
    std::string_view second) {
    // Pattern: one in-place row with a saved diagonal, with empty-prefix lengths zero. Before overwriting cell j preserve its prior-row value; equal bytes extend the prior diagonal by one, otherwise use the greater of prior-row j and current-row j - 1.

    // Finish: return the greatest length of a sequence of bytes appearing in both inputs in the same relative order, not necessarily contiguously; return 0 if either input is empty
}
