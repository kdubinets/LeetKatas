#include <algorithm>
#include <vector>

using namespace std;

struct Interval {
    int start;
    int end;
    bool operator==(const Interval&) const = default;
};

std::vector<Interval> merge_sorted_closed_intervals(const std::vector<Interval>& intervals) {
    // Pattern: one active interval. Sorted starts guarantee that an interval whose start is beyond the active end closes the active interval; otherwise extend its end when needed.

    // Finish: return the union as sorted pairwise nonoverlapping closed intervals; input is sorted by nondecreasing start, every start <= end, intervals sharing an endpoint overlap, empty input returns empty, and input is not modified
}
