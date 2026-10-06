# Name

Unweighted Shortest Distances

# Description

Return a vector with one optional distance per vertex, indexed by vertex identifier. Distances count the fewest directed edges from source; source has distance zero and unreachable vertices have empty optionals. Vertices are indexed from zero through graph.size()-1; graph[v] lists the outgoing neighbors of vertex v, and source and every neighbor are valid indices. Preserve the graph.

Use breadth-first discovery: assign a vertex's distance and mark it discovered when adding it to pending work, so its first discovery gives its shortest distance and it is queued at most once. The learner implements the complete entry function, including distance and frontier initialization.

This exercise covers enqueue-time discovery and distance assignment in unweighted BFS.

# Solution

```cpp
std::vector<std::optional<std::size_t>> distance(graph.size());
std::queue<std::size_t> pending;
distance[source] = 0;
pending.push(source);
while (!pending.empty()) {
    const std::size_t vertex = pending.front();
    pending.pop();
    for (std::size_t neighbor : graph[vertex]) {
        if (!distance[neighbor]) {
            distance[neighbor] = *distance[vertex] + 1;
            pending.push(neighbor);
        }
    }
}
return distance;
```
