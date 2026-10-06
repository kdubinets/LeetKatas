#include <algorithm>
#include <vector>

using namespace std;

struct Interval {
    int start;
    int end;
    bool operator==(const Interval&) const = default;
};

std::vector<Interval> insert_closed_interval(const std::vector<Interval>& intervals, Interval added) {
    // Pattern: three scan phases. Emit intervals strictly before added, absorb every interval overlapping added while expanding its endpoints, emit the merged interval once, then copy the remainder.

    // Finish: return the union of the input intervals and added as maximal nonoverlapping closed intervals sorted by start; input is sorted by start and pairwise nonoverlapping, every interval including added has start <= end, shared endpoints count as overlap, empty input returns {added}, and preserve input
}
