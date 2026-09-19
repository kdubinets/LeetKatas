#include <cstddef>
#include <queue>
#include <vector>

using namespace std;

bool has_bipartite_coloring(const std::vector<std::vector<std::size_t>>& graph) {
    // Pattern: breadth-first two-coloring across every component. Give each uncolored neighbor the opposite color; reject an edge whose endpoints already have the same color.

    // Finish: return whether vertices of the undirected graph can be assigned two colors so every edge joins different colors; every endpoint is valid, reciprocal edges represent each connection, and graph is not modified
}
