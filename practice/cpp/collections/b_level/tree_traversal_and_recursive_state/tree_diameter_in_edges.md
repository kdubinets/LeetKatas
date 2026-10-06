# Name

Tree Diameter through Returned Heights

# Description

Return the greatest number of edges on a simple path between two nodes anywhere in the tree; the path need not pass through the root. Empty and single-node trees have diameter zero. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use postorder traversal with returned subtree heights and a separate greatest-path aggregate. An empty subtree has height zero; the sum of child heights measures the path through their parent. The learner implements the complete entry function, its recursive helper, and aggregate initialization.

This exercise covers returning one subtree summary while updating a separate aggregate.

# Solution

```cpp
std::size_t greatest_path = 0;
auto height = [&](auto&& self, const TreeNode* node) -> std::size_t {
    if (node == nullptr) {
        return 0;
    }
    const std::size_t left = self(self, node->left);
    const std::size_t right = self(self, node->right);
    greatest_path = std::max(greatest_path, left + right);
    return std::max(left, right) + 1;
};
height(height, root);
return greatest_path;
```
