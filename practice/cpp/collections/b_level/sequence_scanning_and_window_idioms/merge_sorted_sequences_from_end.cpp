#include <cstddef>
#include <vector>

using namespace std;

void merge_sorted_into_first(
    std::vector<int>& left,
    std::size_t left_count,
    const std::vector<int>& right) {
    // Pattern: backwards two-pointer merge. Fill reserved output space from the end so unread left values are never overwritten.

    // Finish: fill left with all original values from its first left_count elements and from right in nondecreasing order, preserving duplicates and leaving right unchanged; only the first left_count left elements and all of right are sorted inputs, and remaining left elements are placeholders; the vectors are distinct and left.size() == left_count + right.size() must remain unchanged
}
