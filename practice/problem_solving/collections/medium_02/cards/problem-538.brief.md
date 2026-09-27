# Convert BST to Greater Tree

Given the root of a binary search tree with **unique** keys, change each
node's value to its **original** value plus the sum of all original keys
strictly greater than it. Preserve the tree's shape and return its root.
An empty tree remains empty.

The tree has at most `10^4` nodes. Original keys range from `-10^4` to
`10^4`; each left subtree has smaller keys and each right subtree has larger
keys.
