# Name

Check Bipartite Coloring

# Description

Return whether the undirected adjacency list admits two colors with different colors at the endpoints of every edge, across all components. Vertices are indexed from zero through graph.size()-1; graph[v] lists the neighbors of vertex v, all indices are valid, and connections are reciprocal. Preserve the graph. An empty graph returns true.

Use breadth-first two-coloring: start from every still-uncolored component, assign opposite colors on discovery, and reject a same-color edge. The learner implements the complete entry function, including traversal state.

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
