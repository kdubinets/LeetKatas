# Name

Minimum Step Cost with Memoization

# Description

Return the minimum total cost from index until reaching or passing costs.size(). Pay the cost at every visited in-range position, including the starting position, and advance one or two positions per move. An index already at or beyond the end costs zero. Costs may be negative, must be preserved, and all totals fit in long long.

Use top-down memoization of the supplied recurrence: the current cost plus the smaller of the next two states. Distinguish uncomputed cache entries from computed results, including zero. The learner implements the complete entry function, cache initialization, and any recursive helper.

This exercise covers top-down memoization with an explicit uncomputed cache state.

# Solution

```cpp
std::vector<std::optional<long long>> memo(costs.size());
auto solve = [&](auto&& self, std::size_t position) -> long long {
    if (position >= costs.size()) {
        return 0;
    }
    if (memo[position].has_value()) {
        return *memo[position];
    }
    memo[position] = static_cast<long long>(costs[position]) +
        std::min(self(self, position + 1), self(self, position + 2));
    return *memo[position];
};
return solve(solve, index);
```
