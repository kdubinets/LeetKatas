# Name

Detect a Directed Cycle with Three Colors

# Description

The helper returns whether traversal from a vertex reaches a directed cycle, using zero for unvisited, one for active, and two for complete. Endpoints are valid and the graph is preserved. The wrapper checks all components.

The supplied recursive traversal marks active before descending, detects an edge to active state, skips complete neighbors, and marks complete after all outgoing edges.

This exercise covers three-state distinction between unvisited, active, and completed vertices.

# Solution

```cpp
state[vertex] = 1;
for (std::size_t neighbor : graph[vertex]) {
    if (state[neighbor] == 1) {
        return true;
    }
    if (state[neighbor] == 0 &&
        reaches_active_directed_cycle(neighbor, graph, state)) {
        return true;
    }
}
state[vertex] = 2;
return false;
```
