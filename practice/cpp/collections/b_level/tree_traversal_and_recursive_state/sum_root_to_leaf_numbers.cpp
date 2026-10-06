using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

long long sum_root_to_leaf_numbers(const TreeNode* root) {
    // Pattern: preorder path accumulator. Start with prefix zero and extend it by multiplying by ten and adding the current digit; a leaf contributes that number, while an internal node combines both child contributions.

    // Finish: return the sum of decimal numbers formed by concatenating node digits along every root-to-leaf path; every value is a digit from 0 through 9, an empty tree returns zero, and all intermediate values and the result fit in long long; the tree is finite and acyclic; do not allocate, delete, or modify nodes
}
