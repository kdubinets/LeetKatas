#include <algorithm>
#include <cstddef>
#include <vector>

using namespace std;

std::size_t longest_increasing_subsequence_length(const std::vector<int>& values) {
    // Pattern: predecessor aggregation. State length[i] is the longest strictly increasing subsequence ending at i, initially one; extend every earlier j with values[j] < values[i], then take the greatest state.

    // Finish: return the greatest length of a strictly increasing subsequence, preserving index order without requiring contiguous indices; equal values do not extend it; return 0 for empty input and do not modify values
}
