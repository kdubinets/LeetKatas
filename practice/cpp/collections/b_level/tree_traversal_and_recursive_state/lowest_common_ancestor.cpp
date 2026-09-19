using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

const TreeNode* lowest_common_ancestor(
    const TreeNode* root,
    const TreeNode* first,
    const TreeNode* second) {
    // Pattern: postorder node propagation. Return a target immediately; otherwise combine child results, returning root when both are nonnull and forwarding the sole nonnull result.

    // Finish: return the lowest node whose subtree contains both distinct target nodes by pointer identity; root is nonnull and both targets occur in its finite acyclic tree; do not modify nodes
}
