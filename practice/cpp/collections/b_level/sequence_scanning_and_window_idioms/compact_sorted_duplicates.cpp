#include <cstddef>
#include <vector>

std::size_t compact_sorted_duplicates(std::vector<int>& values) {
    // Pattern: read/write pointers. The prefix before write contains one representative of every completed sorted run.
    // Finish: compact values in place to one copy of each distinct value and return the new length
}
