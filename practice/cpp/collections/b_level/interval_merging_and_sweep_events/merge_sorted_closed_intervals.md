# Name

Merge Sorted Closed Intervals

# Description

Merge all overlapping intervals and return their union as maximal nonoverlapping closed intervals sorted by start. Input starts are nondecreasing, every start <= end, and shared endpoints count as overlap. Empty input returns empty. Preserve the input.

Maintain one active interval: extend it on overlap, emit it when the next start lies beyond its end, and emit the final active interval after the scan.

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
