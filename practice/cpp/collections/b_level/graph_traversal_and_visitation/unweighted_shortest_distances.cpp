#include <cstddef>
#include <optional>
#include <queue>
#include <vector>

using namespace std;

std::vector<std::optional<std::size_t>> unweighted_shortest_distances(
    const std::vector<std::vector<std::size_t>>& graph,
    std::size_t source) {
    // Pattern: breadth-first discovery. Assign a vertex's distance and mark it discovered when enqueueing it, so every vertex enters the queue at most once.

    // Finish: return one entry per vertex containing the fewest directed edges from source, or an empty optional when unreachable; source and every listed endpoint are valid vertex indices and graph is not modified
}
