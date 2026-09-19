#include <cstddef>
#include <deque>
#include <vector>

using namespace std;

std::vector<int> sliding_window_maximum(const std::vector<int>& values, std::size_t width) {
    // Pattern: decreasing deque of candidate indices. Expire indices left of the current window, then discard no-larger values from the back before adding the new index.

    // Finish: return the maximum value of every contiguous group of exactly width elements in left-to-right order; values is nonempty and 1 <= width <= values.size(); do not modify values
}
