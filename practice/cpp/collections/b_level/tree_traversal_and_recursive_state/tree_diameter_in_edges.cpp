#include <algorithm>
#include <cstddef>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

std::size_t tree_diameter_in_edges(const TreeNode* root) {
    // Pattern: postorder returned height plus shared aggregate. An empty subtree has height zero; combine child heights as the edge count of a path through the node, update the greatest path, and return one plus the greater child height.

    // Finish: return the greatest number of edges on any simple path between two nodes in the tree; the path need not pass through root; return zero for an empty or single-node tree; the tree is finite and acyclic; do not allocate, delete, or modify nodes
}
