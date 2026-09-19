# Name

Weighted Shortest Distances with Stale Entries

# Description

Return minimum nonnegative-weight path distances from source, or empty optionals for unreachable vertices. Identifiers are valid, sums fit in long long, and input is preserved.

The supplied tentative-distance heap permits duplicate entries. A popped entry is expanded only if it still equals the recorded best; strict relaxations update and push.

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
