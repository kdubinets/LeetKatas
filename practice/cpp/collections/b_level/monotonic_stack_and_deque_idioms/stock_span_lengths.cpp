#include <cstddef>
#include <vector>

using namespace std;

std::vector<std::size_t> stock_span_lengths(const std::vector<int>& prices) {
    // Pattern: decreasing stack of indices. Remove prior prices less than or equal to the current price; the remaining top is the previous strictly greater boundary.

    // Finish: return for each position the length of the longest contiguous range ending there whose values are all less than or equal to that position's value; return an empty vector for empty input and do not modify prices
}
