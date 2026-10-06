#include <cstddef>
#include <queue>
#include <vector>

using namespace std;

bool has_bipartite_coloring(const std::vector<std::vector<std::size_t>>& graph) {
    // Pattern: breadth-first two-coloring across every component. Give each uncolored neighbor the opposite color; reject an edge whose endpoints already have the same color.

    // Finish: return whether every vertex can receive one of two colors so that every edge joins different colors, across all components; graph[v] lists the neighbors of vertex v with valid indices and reciprocal connections, preserve graph, and an empty graph returns true
}
