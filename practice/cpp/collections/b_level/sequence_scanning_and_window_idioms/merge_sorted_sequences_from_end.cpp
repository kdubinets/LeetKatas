#include <cstddef>
#include <vector>

void merge_sorted_into_first(
    std::vector<int>& left,
    std::size_t left_count,
    const std::vector<int>& right) {
    // Pattern: backwards two-pointer merge. Fill reserved output space from the end so unread left values are never overwritten.
    // Finish: merge the ascending left prefix and ascending right values into left; left has space for both sequences
}
