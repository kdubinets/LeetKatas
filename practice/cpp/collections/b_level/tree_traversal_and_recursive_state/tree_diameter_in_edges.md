# Name

Tree Diameter through Returned Heights

# Description

The helper returns a subtree height in nodes and updates the referenced aggregate with the greatest edge count on any path in that subtree. Null height is zero; the incoming aggregate may already contain a larger outside result. The wrapper returns the whole-tree diameter. Nodes are unchanged.

The supplied postorder pattern separates the summary returned to a parent from the cross-child result accumulated globally.

This exercise covers returning one subtree summary while updating a separate aggregate.

# Solution

```cpp
if (root == nullptr) {
    return 0;
}
const std::size_t left = measure_height_for_diameter(root->left, greatest_path);
const std::size_t right = measure_height_for_diameter(root->right, greatest_path);
greatest_path = std::max(greatest_path, left + right);
return std::max(left, right) + 1;
```
