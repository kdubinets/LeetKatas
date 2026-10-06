# Name

Generate Fixed-Size Increasing Combinations

# Description

Given std::size_t inputs n and k with k <= n, return a vector of every length-k combination of distinct values from 1 through n. Each combination is strictly increasing, and the combinations are in lexicographic order. When k is zero, return one empty combination.

Use increasing-choice backtracking: keep the current path strictly increasing, restore it after each branch, stop at length k, and prune when insufficient values remain. The learner implements the complete function, including its recursive state.

This exercise covers shared-path restoration around increasing recursive choices.

# Solution

```cpp
std::vector<std::vector<std::size_t>> result;
std::vector<std::size_t> path;
auto search = [&](auto&& self, std::size_t start) -> void {
    if (path.size() == k) {
        result.push_back(path);
        return;
    }
    const std::size_t needed = k - path.size();
    // Candidate indices are zero-based; stored values are one-based.
    for (std::size_t index = start; index <= n - needed; ++index) {
        path.push_back(index + 1);
        self(self, index + 1);
        path.pop_back();
    }
};
search(search, 0);
return result;
```
