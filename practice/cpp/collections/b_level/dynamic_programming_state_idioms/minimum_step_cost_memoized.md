# Name

Minimum Step Cost with Memoization

# Description

Return the minimum total cost incurred from index until moving beyond the end. Pay the cost at every visited in-range index, including the starting index, and advance one or two positions per move. An index at or beyond the end costs zero. The memo vector has costs.size() initially disengaged optional entries; the input costs are read-only. Costs may be negative, and all totals fit in long long.

The supplied top-down recurrence adds the current cost to the smaller result obtained after advancing one or two positions. An engaged optional marks a computed state, including a legitimate zero result.

This exercise covers top-down memoization with an explicit uncomputed cache state.

# Solution

```cpp
if (index >= costs.size()) {
    return 0;
}
if (memo[index].has_value()) {
    return *memo[index];
}
memo[index] =
    static_cast<long long>(costs[index]) +
    std::min(
        minimum_step_cost_from(index + 1, costs, memo),
        minimum_step_cost_from(index + 2, costs, memo));
return *memo[index];
```
