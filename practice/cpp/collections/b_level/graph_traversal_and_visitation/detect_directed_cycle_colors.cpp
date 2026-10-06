#include <cstddef>
#include <vector>

using namespace std;

bool has_directed_cycle(const std::vector<std::vector<std::size_t>>& graph) {
    // Pattern: recursive three-state traversal across every component. Mark a vertex active before descending and complete after all outgoing edges; an edge to an active vertex finds a cycle, while complete neighbors need no work.

    // Finish: return whether the directed graph contains a cycle anywhere, including a self-loop; graph[v] lists the outgoing neighbors of vertex v with valid indices, preserve graph, and an empty graph returns false
}
