# Name

Reusable Target-Sum Combinations

# Description

Append every nondecreasing combination summing to the positive initial target. Candidates are strictly increasing and positive, may be reused, and are preserved. Initial state is empty at index zero.

The supplied sorted search reuses the selected index in recursion and stops a loop once a candidate exceeds the remainder.

This exercise covers reusable-choice recursion with sorted overshoot pruning.

# Solution

```cpp
if (remaining == 0) {
    result.push_back(path);
    return;
}
for (std::size_t index = start; index < candidates.size(); ++index) {
    if (candidates[index] > remaining) {
        break;
    }
    path.push_back(candidates[index]);
    collect_target_sum_combinations(
        candidates, index, remaining - candidates[index], path, result);
    path.pop_back();
}
```
