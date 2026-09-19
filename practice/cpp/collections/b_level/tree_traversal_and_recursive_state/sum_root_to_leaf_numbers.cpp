using namespace std;

struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

long long sum_root_to_leaf_numbers(const TreeNode* root, long long prefix = 0) {
    // Pattern: preorder path accumulator. Extend the incoming decimal prefix with the current digit; a leaf contributes that value, while an internal node returns both child contributions.

    // Finish: return the sum of decimal numbers formed along every root-to-leaf path, where every node value is a digit from 0 through 9; return 0 for a null tree, do not modify nodes, and assume all intermediate values and the result fit in long long
}
