#include <cstddef>
#include <functional>
#include <queue>
#include <vector>

using namespace std;

std::vector<double> running_stream_medians(const std::vector<int>& values) {
    // Pattern: maximum heap for the lower half and minimum heap for the upper half. Insert by boundary, then rebalance so lower has either the same size as upper or one extra; their tops determine the prefix median.

    // Finish: return the median after each nonempty input prefix, using the middle value for odd length and the arithmetic mean of the two middle values for even length; return empty for empty input, do not modify values, and avoid integer overflow in the even-prefix sum
}
