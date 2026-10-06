# Name

Validate Strict BST Ancestor Bounds

# Description

Return whether every node has only strictly smaller values throughout its left subtree and strictly larger values throughout its right subtree. Duplicate values are invalid, and values may include the full int range. An empty tree is valid. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use preorder propagation of optional ancestor bounds, initially absent. Each left child inherits a tighter upper bound and each right child a tighter lower bound. The learner implements the complete entry function and any recursive helper.

This exercise covers downward propagation of strict optional ancestor bounds.

# Solution

```cpp
auto valid = [&](auto&& self, const TreeNode* node,
                 std::optional<int> lower, std::optional<int> upper) -> bool {
    if (node == nullptr) {
        return true;
    }
    if ((lower && node->value <= *lower) ||
        (upper && node->value >= *upper)) {
        return false;
    }
    return self(self, node->left, lower, node->value) &&
           self(self, node->right, node->value, upper);
};
return valid(valid, root, std::nullopt, std::nullopt);
```
