#include <algorithm>
#include <cstddef>
#include <optional>

using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

std::optional<std::size_t> balanced_tree_height(const TreeNode* root) {
    // Pattern: postorder optional summary. An empty subtree has height zero; a node returns one plus the greater child height only when both children succeeded and their heights differ by at most one.

    // Finish: return the height in nodes if every node's left and right subtree heights differ by at most one, or an empty optional otherwise; an empty tree has height zero; the tree is finite and acyclic; do not allocate, delete, or modify nodes
}
