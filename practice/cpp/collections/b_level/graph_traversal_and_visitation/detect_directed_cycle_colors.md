# Name

Detect a Directed Cycle with Three Colors

# Description

Return whether the directed adjacency list contains a cycle anywhere, including a self-loop or a cycle unreachable from vertex zero. Vertices are indexed from zero through graph.size()-1; graph[v] lists the outgoing neighbors of vertex v, and all indices are valid. Preserve the graph. An empty graph returns false.

Use recursive traversal with three states: unvisited, active on the current recursion stack, and complete. An edge to an active vertex detects a cycle; an edge to a complete vertex does not. Start traversal at each still-unvisited vertex. The learner implements the complete entry function, including state initialization and any recursive helper.

This exercise covers three-state distinction between unvisited, active, and completed vertices.

# Solution

```cpp
std::vector<int> state(graph.size(), 0);
auto search = [&](auto&& self, std::size_t vertex) -> bool {
    state[vertex] = 1;
    for (std::size_t neighbor : graph[vertex]) {
        if (state[neighbor] == 1) {
            return true;
        }
        if (state[neighbor] == 0 && self(self, neighbor)) {
            return true;
        }
    }
    state[vertex] = 2;
    return false;
};
for (std::size_t vertex = 0; vertex < graph.size(); ++vertex) {
    if (state[vertex] == 0 && search(search, vertex)) {
        return true;
    }
}
return false;
```
