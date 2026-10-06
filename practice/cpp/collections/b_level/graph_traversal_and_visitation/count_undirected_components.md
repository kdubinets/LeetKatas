# Name

Count Undirected Connected Components

# Description

Return the number of connected components in the undirected adjacency list, counting isolated vertices as individual components. Vertices are indexed from zero through graph.size()-1; graph[v] lists the neighbors of vertex v, all indices are valid, and connections are reciprocal. Preserve the graph. An empty graph returns zero.

Use an outer component scan and iterative depth-first traversal: start a component only at an unvisited vertex and mark each neighbor when adding it to pending work. The learner implements the complete entry function, including traversal state.

This exercise covers component-root selection around an iterative visited traversal.

# Solution

```cpp
std::vector<bool> visited(graph.size(), false);
std::size_t components = 0;
for (std::size_t root = 0; root < graph.size(); ++root) {
    if (visited[root]) {
        continue;
    }
    ++components;
    visited[root] = true;
    std::vector<std::size_t> pending{root};
    while (!pending.empty()) {
        const std::size_t vertex = pending.back();
        pending.pop_back();
        for (std::size_t neighbor : graph[vertex]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                pending.push_back(neighbor);
            }
        }
    }
}
return components;
```
