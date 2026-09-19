# Name

Topological Order from Indegree Transitions

# Description

Return a complete topological ordering, or an empty optional if the directed graph has no such ordering. Every endpoint is valid and the graph is preserved. Any valid ordering is accepted.

The supplied indegree frontier enqueues initial zero-indegree vertices and later enqueues a neighbor exactly when decrementing it to zero.

This exercise covers zero-transition maintenance of an indegree frontier.

# Solution

```cpp
std::vector<std::size_t> indegree(graph.size(), 0);
for (const auto& neighbors : graph) {
    for (std::size_t neighbor : neighbors) {
        ++indegree[neighbor];
    }
}
std::queue<std::size_t> ready;
for (std::size_t vertex = 0; vertex < graph.size(); ++vertex) {
    if (indegree[vertex] == 0) {
        ready.push(vertex);
    }
}
std::vector<std::size_t> order;
while (!ready.empty()) {
    const std::size_t vertex = ready.front();
    ready.pop();
    order.push_back(vertex);
    for (std::size_t neighbor : graph[vertex]) {
        if (--indegree[neighbor] == 0) {
            ready.push(neighbor);
        }
    }
}
if (order.size() != graph.size()) {
    return std::nullopt;
}
return order;
```
