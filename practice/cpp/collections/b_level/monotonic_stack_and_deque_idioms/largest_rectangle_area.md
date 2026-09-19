# Name

Largest Rectangle under a Histogram

# Description

Return the greatest area of a contiguous rectangle under nonnegative unit-width histogram bars. Empty input returns zero; preserve heights; areas fit in long long.

The supplied nondecreasing stack stores height and earliest start. A shorter boundary finalizes taller entries and inherits their start; a trailing zero closes remaining positive heights.

This exercise covers earliest-boundary propagation while finalizing monotonic height entries.

# Solution

```cpp
long long best = 0;
std::vector<std::pair<std::size_t, int>> pending;
for (std::size_t index = 0; index <= heights.size(); ++index) {
    const int height = index == heights.size() ? 0 : heights[index];
    std::size_t start = index;
    while (!pending.empty() && pending.back().second > height) {
        const auto [left, prior_height] = pending.back();
        pending.pop_back();
        best = std::max(
            best,
            static_cast<long long>(prior_height) *
                static_cast<long long>(index - left));
        start = left;
    }
    pending.emplace_back(start, height);
}
return best;
```
