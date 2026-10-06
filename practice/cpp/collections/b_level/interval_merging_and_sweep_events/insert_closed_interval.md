# Name

Insert and Merge One Closed Interval

# Description

Return the union of the input intervals and added as maximal nonoverlapping closed intervals sorted by start. The input is sorted by start and pairwise nonoverlapping. Every interval, including added, has start <= end, and shared endpoints count as overlap. Empty input returns a single interval equal to added. Preserve the input.

Use three scan phases: emit intervals before added, absorb overlapping intervals while expanding its endpoints, emit the merged interval once, then copy the remainder.

This exercise covers phase transitions around insertion into sorted disjoint intervals.

# Solution

```cpp
std::vector<Interval> result;
std::size_t index = 0;
while (index < intervals.size() && intervals[index].end < added.start) {
    result.push_back(intervals[index++]);
}
while (index < intervals.size() && intervals[index].start <= added.end) {
    added.start = std::min(added.start, intervals[index].start);
    added.end = std::max(added.end, intervals[index].end);
    ++index;
}
result.push_back(added);
result.insert(result.end(), intervals.begin() + index, intervals.end());
return result;
```
