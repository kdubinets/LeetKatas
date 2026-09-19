#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::size_t union_distinct_roots_by_size(
    std::vector<std::size_t>& parent,
    std::vector<std::size_t>& component_size,
    std::size_t left_root,
    std::size_t right_root) {
    // Pattern: weighted root attachment. Swap roots when needed so left is at least as large, attach right beneath left, and add right's size to left; keep left as winner on equality.

    // Finish: unite the two distinct root components and return the larger root, keeping the original left_root when their sizes are equal; arrays have equal length, both indices are roots with accurate positive sizes, and only the losing root's parent and the surviving root's size may change
}
