# Name

Unweighted Shortest Distances

# Description

Return the fewest directed edges from source to every vertex, or an empty optional if unreachable. All identifiers are valid and the graph is unchanged.

The supplied breadth-first invariant assigns distance at enqueue time, ensuring the first discovery is shortest and each vertex is queued once.

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
