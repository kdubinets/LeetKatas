#include <cstddef>
#include <vector>

using namespace std;

std::size_t count_undirected_components(const std::vector<std::vector<std::size_t>>& graph) {
    // Pattern: outer component scan plus iterative depth-first traversal. Start a component only at an unvisited vertex and mark each neighbor when pushing it.

    // Finish: return the number of connected components, including isolated vertices; graph[v] lists the neighbors of vertex v with valid indices and reciprocal connections, preserve graph, and an empty graph returns zero
}
