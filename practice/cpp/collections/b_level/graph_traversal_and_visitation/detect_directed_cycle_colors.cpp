#include <cstddef>
#include <vector>

using namespace std;

bool reaches_active_directed_cycle(
    std::size_t vertex,
    const std::vector<std::vector<std::size_t>>& graph,
    std::vector<int>& state) {
    // Pattern: recursive three-color traversal. Mark vertex active before descending; an edge to active state finds a cycle, complete neighbors need no work, and a fully explored vertex becomes complete.

    // Finish: return whether traversal from vertex reaches a directed cycle, using state 0 for unvisited, 1 for active on the current recursion stack, and 2 for complete; every endpoint is valid and graph is not modified
}

bool has_directed_cycle(const std::vector<std::vector<std::size_t>>& graph) {
    std::vector<int> state(graph.size(), 0);
    for (std::size_t vertex = 0; vertex < graph.size(); ++vertex) {
        if (state[vertex] == 0 &&
            reaches_active_directed_cycle(vertex, graph, state)) {
            return true;
        }
    }
    return false;
}
