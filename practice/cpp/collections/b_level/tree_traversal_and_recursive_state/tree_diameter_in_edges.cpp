#include <algorithm>
#include <cstddef>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

std::size_t measure_height_for_diameter(const TreeNode* root, std::size_t& greatest_path) {
    // Pattern: postorder returned height plus shared aggregate. Empty height is zero; combine child heights as a path through the node before returning one plus their maximum.

    // Finish: return root's subtree height in nodes and update greatest_path to the greatest number of edges on any path found in that subtree; root may be null, greatest_path contains the best value found outside this subtree, and nodes are not modified
}

std::size_t tree_diameter_in_edges(const TreeNode* root) {
    std::size_t greatest_path = 0;
    measure_height_for_diameter(root, greatest_path);
    return greatest_path;
}
