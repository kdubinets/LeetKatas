# Name

Check Bipartite Coloring

# Description

Return whether the undirected graph admits two colors with different colors on every edge. Endpoints are valid and connections reciprocal. Empty and disconnected graphs are allowed; preserve the graph.

The supplied traversal starts from every uncolored component, assigns opposite colors on discovery, and rejects a same-color edge.

This exercise covers two-color discovery state and conflict detection across components.

# Solution

```cpp
std::vector<int> color(graph.size(), -1);
for (std::size_t root = 0; root < graph.size(); ++root) {
    if (color[root] != -1) {
        continue;
    }
    color[root] = 0;
    std::queue<std::size_t> pending;
    pending.push(root);
    while (!pending.empty()) {
        const std::size_t vertex = pending.front();
        pending.pop();
        for (std::size_t neighbor : graph[vertex]) {
            if (color[neighbor] == -1) {
                color[neighbor] = 1 - color[vertex];
                pending.push(neighbor);
            } else if (color[neighbor] == color[vertex]) {
                return false;
            }
        }
    }
}
return true;
```
