#include <cstddef>
#include <optional>
#include <queue>
#include <vector>

using namespace std;

std::vector<std::optional<std::size_t>> unweighted_shortest_distances(
    const std::vector<std::vector<std::size_t>>& graph,
    std::size_t source) {
    // Pattern: breadth-first discovery. Assign a vertex's distance and mark it discovered when enqueueing it, so every vertex enters the queue at most once.

    // Finish: return one entry per vertex containing the fewest directed edges from source, with distance zero for source and an empty optional for unreachable vertices; graph[v] lists the outgoing neighbors of vertex v, source and every neighbor are valid vertex indices, and preserve graph
}
