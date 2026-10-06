# Name

Topological Order from Indegree Transitions

# Description

Return an optional containing any ordering of all vertices exactly once such that each directed edge's source precedes its destination. Return an empty optional if the graph contains a cycle. Vertices are indexed from zero through graph.size()-1; graph[v] lists the outgoing neighbors of vertex v, and all indices are valid. Preserve the graph. An empty graph returns an optional containing an empty vector.

Use an indegree frontier: initialize each vertex's indegree from the adjacency lists, start with every zero-indegree vertex, and add a neighbor exactly when its decremented indegree reaches zero. Failure to process all vertices means no ordering exists. The learner implements the complete entry function, including indegree and frontier initialization.

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
