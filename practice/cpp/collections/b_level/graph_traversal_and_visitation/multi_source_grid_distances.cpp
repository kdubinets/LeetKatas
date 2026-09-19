#include <cstddef>
#include <optional>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

std::vector<std::vector<std::optional<std::size_t>>> multi_source_grid_distances(
    const std::vector<std::vector<int>>& grid) {
    // Pattern: multi-source breadth-first discovery. Enqueue every cell whose value is one with distance zero before expanding; assign each undiscovered four-neighbor when enqueueing it.

    // Finish: return for every cell its fewest four-direction moves to any cell whose value is 1, or an empty optional if the grid contains no such source; grid is nonempty and rectangular with at least one column and is not modified
}
