# Name

Find a Root with Path Halving

# Description

Return the root reached from node in a valid rooted parent forest, where each root points to itself and node is a valid index. Redirect each visited nonroot to its current grandparent and continue from that shortened position. Preserve vector size and every unvisited entry. A root query returns that root without changing the forest.

Use iterative path halving while walking to the root; the changed links preserve the original component membership.

This exercise covers iterative root finding with path-halving compression.

# Solution

```cpp
while (parent[node] != node) {
    parent[node] = parent[parent[node]];
    node = parent[node];
}
return node;
```
