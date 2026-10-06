# Name

Intersect Two Sorted Closed-Interval Lists

# Description

Return all nonempty pairwise intersections between the two closed-interval lists, sorted by start. Each input is sorted by start and pairwise nonoverlapping, and every interval has start <= end. Shared endpoints form one-point intersections. Either empty input returns empty. Preserve both inputs.

Use paired interval frontiers: emit an overlap, then advance the interval that ends first because it cannot overlap a later counterpart; advance both when their ends are equal.

This exercise covers paired-frontier advancement after closed-interval intersection.

# Solution

```cpp
std::vector<Interval> result;
std::size_t left_index = 0;
std::size_t right_index = 0;
while (left_index < left.size() && right_index < right.size()) {
    const int start = std::max(left[left_index].start, right[right_index].start);
    const int end = std::min(left[left_index].end, right[right_index].end);
    if (start <= end) {
        result.push_back({start, end});
    }
    if (left[left_index].end < right[right_index].end) {
        ++left_index;
    } else if (right[right_index].end < left[left_index].end) {
        ++right_index;
    } else {
        ++left_index;
        ++right_index;
    }
}
return result;
```
