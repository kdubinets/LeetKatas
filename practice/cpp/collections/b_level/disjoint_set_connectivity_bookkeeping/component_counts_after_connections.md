# Name

Component Counts after Connections

# Description

Return the connected-component count after every connection, starting with isolated vertices. Endpoints are valid; repeated and self connections are allowed; preserve input.

The supplied union helper reports whether connectivity actually changed. The running count decrements only on successful unions.

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
