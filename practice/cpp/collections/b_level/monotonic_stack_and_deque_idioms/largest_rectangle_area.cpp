#include <algorithm>
#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

long long largest_rectangle_area(const std::vector<int>& heights) {
    // Pattern: nondecreasing stack of {start, height}. When a shorter height arrives, finalize taller entries and carry their earliest start forward; a trailing zero finalizes remaining positive heights.

    // Finish: return the greatest area of a contiguous rectangle under nonnegative bar heights with unit bar widths; return 0 for empty input, do not modify heights, and assume every area fits in long long
}
