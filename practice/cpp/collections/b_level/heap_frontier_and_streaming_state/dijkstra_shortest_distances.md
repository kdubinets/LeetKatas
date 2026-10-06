# Name

Weighted Shortest Distances with Stale Entries

# Description

Return one optional distance per vertex, indexed by zero-based vertex identifier. Each distance is the minimum total directed-edge weight from source; source has distance zero and unreachable vertices have empty optionals. Graph[v] lists outgoing edges, source and all endpoints are valid, and weights are nonnegative. Preserve graph. All evaluated distance-plus-weight sums fit in long long.

Use a minimum heap of tentative distance/vertex entries. Multiple entries for one vertex are allowed; expand an entry only if its distance still equals the recorded best, and record and enqueue each strict improvement. The learner implements the complete entry function and frontier initialization.

This exercise covers stale-entry filtering in a weighted shortest-path heap frontier.

# Solution

```cpp
using Entry = std::pair<long long, std::size_t>;
std::priority_queue<Entry, std::vector<Entry>, std::greater<>> frontier;
std::vector<std::optional<long long>> distance(graph.size());
distance[source] = 0;
frontier.emplace(0, source);
while (!frontier.empty()) {
    const auto [current_distance, vertex] = frontier.top();
    frontier.pop();
    if (!distance[vertex] || current_distance != *distance[vertex]) {
        continue;
    }
    for (const WeightedEdge& edge : graph[vertex]) {
        const long long candidate = current_distance + edge.weight;
        if (!distance[edge.to] || candidate < *distance[edge.to]) {
            distance[edge.to] = candidate;
            frontier.emplace(candidate, edge.to);
        }
    }
}
return distance;
```
