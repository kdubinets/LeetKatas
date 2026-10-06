# Name

Balanced Tree Height or Failure

# Description

Return the height in nodes when every node's left and right subtree heights differ by at most one, or an empty optional otherwise. An empty tree has height zero. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use a postorder optional summary to propagate either a subtree height or failure in one traversal. The learner implements the complete entry function.

This exercise covers postorder propagation of either a height or a failure state.

# Solution

```cpp
if (root == nullptr) {
    return 0;
}
const auto left = balanced_tree_height(root->left);
if (!left) {
    return std::nullopt;
}
const auto right = balanced_tree_height(root->right);
if (!right || (*left > *right ? *left - *right : *right - *left) > 1) {
    return std::nullopt;
}
return std::max(*left, *right) + 1;
```
