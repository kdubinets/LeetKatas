# Binary Tree Right Side View

Given the root of a binary tree, return the values visible when viewing the
tree from its right side, ordered from top to bottom. At each depth, only the
furthest-right node that exists at that depth is visible. A node in the left
subtree can still be visible when nothing lies to its right at that depth.

For example, this tree has right-side view `[1, 3, 4, 5]`:

```text
       1
      / \
     2   3
    /
   4
  /
 5
```

The tree may be empty, in which case return an empty list. It contains at most
100 nodes, with node values between `-100` and `100`.
