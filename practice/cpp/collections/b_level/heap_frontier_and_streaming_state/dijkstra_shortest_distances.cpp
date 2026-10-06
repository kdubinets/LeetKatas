#include <cstddef>
#include <functional>
#include <optional>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

struct WeightedEdge {
    std::size_t to;
    long long weight;
};

std::vector<std::optional<long long>> dijkstra_shortest_distances(
    const std::vector<std::vector<WeightedEdge>>& graph,
    std::size_t source) {
    // Pattern: minimum heap of tentative {distance, vertex}. Skip an entry unless its distance still equals the recorded best; relax each nonnegative outgoing edge and push every strict improvement.

    // Finish: return one optional distance per vertex, indexed by vertex, containing the minimum total directed-edge weight from source, zero for source, or an empty optional when unreachable; graph[v] lists outgoing edges, source and endpoints are valid indices, weights are nonnegative, all evaluated distance-plus-weight sums fit in long long, and preserve graph
}
