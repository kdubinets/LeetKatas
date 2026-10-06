#include <cstddef>
#include <optional>
#include <queue>
#include <vector>

using namespace std;

std::optional<std::vector<std::size_t>> topological_order(
    const std::vector<std::vector<std::size_t>>& graph) {
    // Pattern: indegree frontier. Enqueue every initial zero-indegree vertex; after removing a vertex, decrement each outgoing neighbor and enqueue that neighbor exactly on its transition to zero.

    // Finish: return any ordering containing every vertex exactly once with each directed edge's source before its destination, or an empty optional if the graph contains a cycle; graph[v] lists the outgoing neighbors of vertex v with valid indices, preserve graph, and an empty graph returns an optional containing an empty vector
}
