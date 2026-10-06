# Name

Sum Root-to-Leaf Digit Numbers

# Description

Return the sum of decimal numbers formed by concatenating the digits along each root-to-leaf path. Each node value is a digit from 0 through 9; leading zeroes do not change a number's value. An empty tree contributes zero, and all intermediate values and the result fit in long long. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use preorder accumulation starting with prefix zero. Extend the prefix at each node, contribute the completed number at a leaf, and combine child contributions otherwise. The learner implements the complete entry function and its recursive state.

This exercise covers downward extension of a path accumulator with leaf finalization.

# Solution

```cpp
auto sum = [&](auto&& self, const TreeNode* node, long long prefix) -> long long {
    if (node == nullptr) {
        return 0;
    }
    const long long current = prefix * 10 + node->value;
    if (node->left == nullptr && node->right == nullptr) {
        return current;
    }
    return self(self, node->left, current) + self(self, node->right, current);
};
return sum(sum, root, 0);
```
