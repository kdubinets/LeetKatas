# Name

Kth Value in Inorder Traversal

# Description

Return the value at the valid positive one-based rank in inorder traversal. The tree is nonempty and large enough; nodes are caller-owned and unchanged.

The supplied explicit stack suspends ancestors during left descent, then resumes each visit before entering its right subtree.

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
