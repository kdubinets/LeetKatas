# Name

Count Undirected Connected Components

# Description

Return the number of connected components, including isolated vertices, in the supplied undirected adjacency list. Endpoints are valid and connections are reciprocal. Preserve the graph.

The supplied outer scan starts one iterative traversal per unvisited root; vertices are marked when pushed to avoid duplicate pending work.

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
