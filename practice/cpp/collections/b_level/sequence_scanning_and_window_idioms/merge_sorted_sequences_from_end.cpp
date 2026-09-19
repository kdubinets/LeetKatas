#include <cstddef>
#include <vector>

using namespace std;

void merge_sorted_into_first(
    std::vector<int>& left,
    std::size_t left_count,
    const std::vector<int>& right) {
    // Pattern: backwards two-pointer merge. Fill reserved output space from the end so unread left values are never overwritten.

    // Finish: left must contain all original values from its first left_count elements and from right, in nondecreasing order, including duplicates; both input sequences are sorted; left.size() equals left_count + right.size() and must stay unchanged
}
