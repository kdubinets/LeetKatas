#include <algorithm>
#include <cstddef>
#include <utility>
#include <vector>

using namespace std;

struct Interval {
    int start;
    int end;
    bool operator==(const Interval&) const = default;
};

std::size_t minimum_half_open_meeting_rooms(const std::vector<Interval>& meetings) {
    // Pattern: sorted event sweep. Represent starts as +1 and ends as -1; at equal times process end events first because meetings are half-open, then track the greatest active count.

    // Finish: return the minimum number of rooms needed so every half-open meeting [start, end) can run, where start < end and a meeting ending when another starts may share its room; return 0 for empty input and do not modify meetings
}
