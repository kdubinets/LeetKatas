# Name

Component Counts after Connections

# Description

Return one connected-component count per connection in input order, starting with vertex_count isolated vertices indexed from zero through vertex_count-1. Connections are undirected, all endpoints are valid, and repeated or self connections are allowed. No connections returns an empty result. Preserve connections.

The supplied union operation returns true exactly when it merges two previously separate components. Initialize the parent forest and component sizes, then decrement the running count only after a successful union. Supporting find and union implementations are supplied to isolate component-count bookkeeping.

This exercise covers component-count maintenance conditioned on successful unions.

# Solution

```cpp
std::vector<std::size_t> parent(vertex_count);
std::iota(parent.begin(), parent.end(), 0);
std::vector<std::size_t> size(vertex_count, 1);
std::size_t components = vertex_count;
std::vector<std::size_t> result;
result.reserve(connections.size());
for (const auto& [left, right] : connections) {
    if (dsu_unite(parent, size, left, right)) {
        --components;
    }
    result.push_back(components);
}
return result;
```
