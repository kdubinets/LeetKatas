# Name

Shortest Sufficient Subarray with Negative Values

# Description

Return the shortest nonempty contiguous range length whose sum reaches the positive target, or an empty optional if none exists. Values may be negative, sums fit in long long, and the input is preserved.

The supplied increasing prefix-index deque has separate rules: satisfactory front indices produce answers, while no-smaller back prefixes are dominated by the current prefix.

This exercise covers two-ended maintenance of satisfactory and dominated prefix candidates.

# Solution

```cpp
std::deque<std::size_t> candidates;
std::vector<long long> prefix(values.size() + 1, 0);
std::optional<std::size_t> best;
for (std::size_t index = 0; index <= values.size(); ++index) {
    if (index > 0) {
        prefix[index] = prefix[index - 1] + values[index - 1];
    }
    while (!candidates.empty() &&
           prefix[index] - prefix[candidates.front()] >= target) {
        const std::size_t length = index - candidates.front();
        best = best.has_value() ? std::min(*best, length) : length;
        candidates.pop_front();
    }
    while (!candidates.empty() &&
           prefix[candidates.back()] >= prefix[index]) {
        candidates.pop_back();
    }
    candidates.push_back(index);
}
return best;
```
