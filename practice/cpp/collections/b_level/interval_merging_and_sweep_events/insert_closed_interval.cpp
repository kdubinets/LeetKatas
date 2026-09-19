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

    // Finish: insert added and return the union as sorted pairwise nonoverlapping closed intervals; input is sorted and pairwise nonoverlapping, all intervals have start <= end, intervals sharing an endpoint overlap, and input is not modified
}
