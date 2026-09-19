#include <cstddef>
#include <vector>

using namespace std;

std::size_t compact_sorted_duplicates(std::vector<int>& values) {
    // Pattern: read/write pointers. The written prefix contains each distinct value encountered so far exactly once, in input order.

    // Finish: modify values so its prefix contains each distinct input value once, in sorted order; return this prefix's length; keep values.size() unchanged, with remaining elements unspecified; input is sorted in nondecreasing order
}
