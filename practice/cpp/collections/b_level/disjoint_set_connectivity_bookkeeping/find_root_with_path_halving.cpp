#include <cstddef>
#include <vector>

using namespace std;

std::size_t find_root_with_path_halving(std::vector<std::size_t>& parent, std::size_t node) {
    // Pattern: iterative path halving. While node is not a root, redirect it to its grandparent and continue from that shortened position.

    // Finish: return the root reached from node, redirect each visited nonroot to its current grandparent before continuing from that shortened position, and leave unvisited entries unchanged; parent represents a valid rooted forest with parent[root] == root and node is a valid index
}
