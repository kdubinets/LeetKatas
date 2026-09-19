#include <algorithm>
#include <cstddef>
#include <queue>
#include <vector>

using namespace std;

std::vector<int> retain_k_smallest_values(const std::vector<int>& values, std::size_t count) {
    // Pattern: bounded maximum heap. Add each value, then remove the heap maximum whenever size exceeds count; the heap therefore retains the smallest count values seen so far.

    // Finish: return the smallest count input values in nondecreasing order, preserving duplicate multiplicity; count <= values.size(), return empty when count is 0, and do not modify values
}
