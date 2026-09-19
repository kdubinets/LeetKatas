# Name

Lowest Common Ancestor by Postorder Propagation

# Description

Return the lowest node whose subtree contains both distinct target nodes, using pointer identity. Both targets are present in the nonempty finite tree. Nodes are unchanged.

The supplied postorder propagation returns a target immediately, combines two nonnull child results at their first meeting node, and otherwise forwards the sole result.

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
