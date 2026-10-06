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

    // Finish: merge all overlapping intervals and return their union as maximal nonoverlapping closed intervals sorted by start; input starts are nondecreasing, every start <= end, shared endpoints count as overlap, empty input returns empty, and preserve input
}
