#include <optional>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

bool subtree_respects_strict_bounds(
    const TreeNode* root,
    std::optional<int> lower,
    std::optional<int> upper) {
    // Pattern: preorder ancestor context. Reject a value not strictly between its optional bounds; pass the current value as the upper bound on the left and lower bound on the right.

    // Finish: return whether every node in root's subtree is strictly greater than lower when present and strictly less than upper when present, with the same rule recursively applied; a null subtree is valid and nodes are not modified
}

bool is_strict_binary_search_tree(const TreeNode* root) {
    return subtree_respects_strict_bounds(root, std::nullopt, std::nullopt);
}
