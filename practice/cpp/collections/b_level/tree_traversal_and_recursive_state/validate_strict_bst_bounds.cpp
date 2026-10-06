#include <optional>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

bool is_strict_binary_search_tree(const TreeNode* root) {
    // Pattern: preorder ancestor bounds. Begin with no bounds; reject any value outside its strict optional bounds, then pass the current value as the upper bound on the left and lower bound on the right.

    // Finish: return whether every node has only smaller values throughout its left subtree and only larger values throughout its right subtree; duplicate values are invalid and all int values are allowed; an empty tree is valid; the tree is finite and acyclic; do not allocate, delete, or modify nodes
}
