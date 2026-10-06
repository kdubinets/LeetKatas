# Name

Reusable Target-Sum Combinations

# Description

Return every distinct nondecreasing combination whose values sum to the positive target. Candidates are strictly increasing and positive, may be reused any number of times, and are preserved. Return an empty result when no combination exists; result order is unspecified.

Use sorted reusable-choice backtracking, restoring the path after each branch and stopping candidate exploration on overshoot. The learner implements the complete function and its recursive state.

This exercise covers reusable-choice recursion with sorted overshoot pruning.

# Solution

```cpp
std::vector<std::vector<int>> result;
std::vector<int> path;
auto search = [&](auto&& self, std::size_t start, int remaining) -> void {
    if (remaining == 0) {
        result.push_back(path);
        return;
    }
    for (std::size_t index = start; index < candidates.size(); ++index) {
        if (candidates[index] > remaining) {
            break;
        }
        path.push_back(candidates[index]);
        self(self, index, remaining - candidates[index]);
        path.pop_back();
    }
};
search(search, 0, target);
return result;
```
