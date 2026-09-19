# Name

Balanced Tree Height or Failure

# Description

Return the height in nodes if every node's child-subtree heights differ by at most one, or an empty optional otherwise. Empty tree height is zero. Nodes are caller-owned and unchanged.

The supplied postorder summary carries either a subtree height or failure, allowing failure to propagate without a separate traversal.

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
