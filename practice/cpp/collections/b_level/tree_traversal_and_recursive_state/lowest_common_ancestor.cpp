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

    // Finish: return the deepest node whose subtree contains both distinct target nodes, counting a node as part of its own subtree and identifying targets by pointer identity; root is nonnull and both targets occur in the tree; the tree is finite and acyclic; do not allocate, delete, or modify nodes
}
