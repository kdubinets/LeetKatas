# Name

Sum Root-to-Leaf Digit Numbers

# Description

Return the sum of decimal numbers formed by all root-to-leaf digit paths. The prefix parameter is the already formed number above root. Null contributes zero; node values are digits; arithmetic fits in long long. Nodes are unchanged.

The supplied preorder accumulator extends the prefix at each node, contributes at leaves, and combines child results otherwise.

This exercise covers downward extension of a path accumulator with leaf finalization.

# Solution

```cpp
if (root == nullptr) {
    return 0;
}
const long long current = prefix * 10 + root->value;
if (root->left == nullptr && root->right == nullptr) {
    return current;
}
return sum_root_to_leaf_numbers(root->left, current) +
       sum_root_to_leaf_numbers(root->right, current);
```
