# Find Subtree Sizes After Changes

A tree rooted at node 0 is given by `parent`, where `parent[0]=-1`, and each node has a lowercase letter `s[i]`. **Simultaneously**, each nonroot node changes its parent to its closest ancestor in the **original** tree with the same letter, if such an ancestor exists; otherwise its parent stays. Return the size of every node's subtree in the **final** tree. The tree has up to 100,000 nodes and may be a chain.

For `parent=[-1,0,4,0,1]`, `s='abbba'`, nodes 4 and 2 move to original ancestors 0 and 1 respectively; final subtree sizes are `[5,2,1,1,1]`.
