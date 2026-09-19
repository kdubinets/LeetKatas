#include <cstddef>
#include <vector>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

int kth_inorder_value(const TreeNode* root, std::size_t rank) {
    // Pattern: iterative inorder suspension. Descend left while stacking nodes, then visit and move right; decrement the one-based rank at each visit and stop when it reaches zero.

    // Finish: return the value of the node visited at one-based position rank in inorder traversal; root is nonnull and contains at least rank nodes, rank is positive, and nodes are not modified
}
