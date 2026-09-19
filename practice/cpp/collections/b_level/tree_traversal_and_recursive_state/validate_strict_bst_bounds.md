# Name

Validate Strict BST Ancestor Bounds

# Description

Return whether the subtree obeys the supplied optional strict bounds recursively. Null is valid. The wrapper therefore validates a strict binary-search tree; duplicate values are invalid. Optional bounds safely represent trees containing extreme int values. Nodes are unchanged.

The supplied preorder context narrows the upper bound for a left child and the lower bound for a right child.

This exercise covers downward propagation of strict optional ancestor bounds.

# Solution

```cpp
if (root == nullptr) {
    return true;
}
if ((lower && root->value <= *lower) ||
    (upper && root->value >= *upper)) {
    return false;
}
return subtree_respects_strict_bounds(root->left, lower, root->value) &&
       subtree_respects_strict_bounds(root->right, root->value, upper);
```
