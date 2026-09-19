# Name

Insert and Merge One Closed Interval

# Description

Insert added and return the union as sorted pairwise nonoverlapping closed intervals. Input is already sorted and pairwise nonoverlapping; all endpoints are valid and shared endpoints overlap. Preserve input.

The supplied three-phase scan emits intervals before added, absorbs overlapping intervals into it, emits it once, and copies the remainder.

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
