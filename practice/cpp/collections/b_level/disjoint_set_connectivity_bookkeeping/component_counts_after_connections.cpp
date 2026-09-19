#include <cstddef>
#include <numeric>
#include <utility>
#include <vector>

using namespace std;

std::size_t dsu_find(std::vector<std::size_t>& parent, std::size_t node) {
    while (parent[node] != node) {
        parent[node] = parent[parent[node]];
        node = parent[node];
    }
    return node;
}

bool dsu_unite(
    std::vector<std::size_t>& parent,
    std::vector<std::size_t>& size,
    std::size_t left,
    std::size_t right) {
    left = dsu_find(parent, left);
    right = dsu_find(parent, right);
    if (left == right) {
        return false;
    }
    if (size[left] < size[right]) {
        std::swap(left, right);
    }
    parent[right] = left;
    size[left] += size[right];
    return true;
}

std::vector<std::size_t> component_counts_after_connections(
    std::size_t vertex_count,
    const std::vector<std::pair<std::size_t, std::size_t>>& connections) {
    // Pattern: successful-union bookkeeping. Begin with one component per vertex and decrement only when the supplied union operation returns true.

    // Finish: return the number of connected components after each connection is processed in order, starting from vertex_count isolated vertices; every endpoint is valid, repeated and self connections are allowed, and connections is not modified
}
