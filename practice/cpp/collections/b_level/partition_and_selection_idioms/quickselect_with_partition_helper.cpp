#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

/*
Supporting partition primitive: low <= high < values.size().
Only [low, high] is rearranged, preserving its values and placing the original
last-element pivot at the returned index, with smaller values before it and
values greater than or equal to it after it.
*/
std::size_t partition_around_last(
    std::vector<int>& values,
    std::size_t low,
    std::size_t high) {
    const int pivot = values[high];
    std::size_t boundary = low;
    for (std::size_t index = low; index < high; ++index) {
        if (values[index] < pivot) {
            std::swap(values[boundary++], values[index]);
        }
    }
    std::swap(values[boundary], values[high]);
    return boundary;
}

int quickselect_with_partition_helper(
    std::vector<int>& values,
    std::size_t rank) {
    // Pattern: inclusive quickselect range. Partition the current range with the supplied last-element helper; return on rank, otherwise discard the side that cannot contain the zero-based sorted rank.

    // Finish: return the value at zero-based position rank in nondecreasing sorted order while allowing values to be rearranged; values is nonempty, rank < values.size(), duplicate values are allowed, and vector size and multiplicities must remain unchanged
}
