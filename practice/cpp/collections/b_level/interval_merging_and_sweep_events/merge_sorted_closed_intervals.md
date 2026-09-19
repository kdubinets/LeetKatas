# Name

Merge Sorted Closed Intervals

# Description

Return the union as sorted pairwise nonoverlapping closed intervals. Input starts are nondecreasing, endpoints are valid, and sharing an endpoint counts as overlap. Empty input remains empty and input is preserved.

The supplied scan maintains one active interval, extending it on overlap and emitting it only after a later start lies beyond its end.

This exercise covers extension and finalization of one active sorted interval.

# Solution

```cpp
if (intervals.empty()) {
    return {};
}
std::vector<Interval> merged;
Interval active = intervals.front();
for (std::size_t index = 1; index < intervals.size(); ++index) {
    if (intervals[index].start <= active.end) {
        active.end = std::max(active.end, intervals[index].end);
    } else {
        merged.push_back(active);
        active = intervals[index];
    }
}
merged.push_back(active);
return merged;
```
