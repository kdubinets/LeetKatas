#include <algorithm>
#include <vector>

using namespace std;

struct Interval {
    int start;
    int end;
    bool operator==(const Interval&) const = default;
};

std::vector<Interval> intersect_sorted_closed_intervals(const std::vector<Interval>& left, const std::vector<Interval>& right) {
    // Pattern: paired interval frontiers. Emit the overlap when max(starts) <= min(ends), then advance the interval with the smaller end, advancing both when ends are equal.

    // Finish: return all nonempty intersections between closed intervals from left and right in sorted order; each input is sorted and pairwise nonoverlapping with valid endpoints, shared endpoints form one-point intersections, and inputs are not modified
}
