#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

long long maximum_container_area(const std::vector<int>& heights) {
    // Pattern: converging two pointers. After measuring a pair, discard the endpoint with the smaller height; either endpoint may be discarded when heights are equal.

    // Finish: return the maximum area over pairs of indices i < j, where area is (j - i) times the smaller of heights[i] and heights[j]; heights are nonnegative; return zero if fewer than two elements exist
}
