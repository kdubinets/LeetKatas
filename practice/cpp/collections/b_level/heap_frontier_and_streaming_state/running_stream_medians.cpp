#include <cstddef>
#include <functional>
#include <queue>
#include <vector>

using namespace std;

std::vector<double> running_stream_medians(const std::vector<int>& values) {
    // Pattern: maximum heap for the lower half and minimum heap for the upper half, initially empty. Every lower-half value is at most every upper-half value; rebalance after insertion so lower has the same size or one extra, then read the prefix median from their boundaries.

    // Finish: return one median per input element in prefix order; after sorting each nonempty prefix, use its middle value for odd length or the arithmetic mean of its two middle values for even length; empty input returns empty, preserve values, and avoid integer overflow when averaging
}
