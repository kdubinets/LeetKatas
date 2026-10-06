#include <cstddef>
#include <optional>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

std::vector<std::vector<std::optional<std::size_t>>> multi_source_grid_distances(
    const std::vector<std::vector<int>>& grid) {
    // Pattern: multi-source breadth-first discovery. Enqueue every cell whose value is one with distance zero before expanding; assign each undiscovered four-neighbor when enqueueing it.

    // Finish: return a grid of the same dimensions containing each cell's fewest horizontal or vertical moves to any cell whose value is 1, with source cells at distance zero and every entry an empty optional if there is no source; all cells are traversable regardless of value, grid is nonempty and rectangular with at least one column, and preserve grid
}
