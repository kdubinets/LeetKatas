#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

std::pair<std::size_t, std::size_t> three_way_partition_around_pivot(
    std::vector<int>& values,
    int pivot) {
    // Pattern: four regions with boundaries less, scan, and greater: [0, less) is below pivot, [less, scan) equals pivot, [scan, greater) is unknown, and [greater, size) is above pivot.

    // Finish: rearrange values in place into below-pivot, equal-pivot, and above-pivot regions; return zero-based {equal_begin, equal_end} for the half-open equal region, preserve size and multiplicities, and allow arbitrary order within each region; absent pivot gives an empty equal region at the boundary after all smaller values, and empty input returns {0, 0}
}
