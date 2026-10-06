# Name

Lowest Common Ancestor by Postorder Propagation

# Description

Return the deepest node whose subtree contains both distinct targets, identified by pointer identity rather than stored value. A node belongs to its own subtree, so a target may itself be the answer. Both targets occur in the nonempty tree. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use postorder node propagation: return a target immediately, combine two nonnull child results at their meeting node, and otherwise forward the sole result. The learner implements the complete entry function.

This exercise covers postorder propagation and combination of child node results.

# Solution

```cpp
if (root == nullptr || root == first || root == second) {
    return root;
}
const TreeNode* left =
    lowest_common_ancestor(root->left, first, second);
const TreeNode* right =
    lowest_common_ancestor(root->right, first, second);
if (left != nullptr && right != nullptr) {
    return root;
}
return left != nullptr ? left : right;
```
