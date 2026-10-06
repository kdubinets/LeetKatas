#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::size_t union_distinct_roots_by_size(
    std::vector<std::size_t>& parent,
    std::vector<std::size_t>& component_size,
    std::size_t left_root,
    std::size_t right_root) {
    // Pattern: weighted root attachment. Attach the smaller component beneath the larger and add its size to the surviving root; the original left root survives on equal sizes.

    // Finish: unite the two distinct root components and return the root of the component with more vertices, retaining original left_root on equal sizes; parent is a valid rooted forest, component_size has equal length and accurate positive sizes at roots, and both indices are valid distinct roots; change only the losing root's parent and the surviving root's size
}
