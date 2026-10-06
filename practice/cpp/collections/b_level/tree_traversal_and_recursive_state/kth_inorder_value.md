# Name

Kth Value in Inorder Traversal

# Description

Return the value at a valid positive one-based rank in inorder traversal: visit the left subtree, the node, then the right subtree. The tree is nonempty and has at least rank nodes; its values need not be sorted or distinct. The input is a caller-owned finite acyclic binary tree. Do not allocate, delete, or modify nodes.

Use iterative inorder traversal with an explicit stack to suspend ancestors during left descent and resume each visit before entering its right subtree. The learner implements the complete entry function.

This exercise covers explicit suspension and resumption of iterative inorder traversal.

# Solution

```cpp
std::vector<const TreeNode*> pending;
const TreeNode* current = root;
while (true) {
    while (current != nullptr) {
        pending.push_back(current);
        current = current->left;
    }
    current = pending.back();
    pending.pop_back();
    if (--rank == 0) {
        return current->value;
    }
    current = current->right;
}
```
