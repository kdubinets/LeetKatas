# Name

Find a Root with Path Halving

# Description

Return the root reached from the valid node in a valid parent forest and shorten links along the queried path. Each root is its own parent.

The supplied iterative path-halving invariant redirects a visited nonroot to its grandparent before continuing.

This exercise covers iterative root finding with path-halving compression.

# Solution

```cpp
while (parent[node] != node) {
    parent[node] = parent[parent[node]];
    node = parent[node];
}
return node;
```
