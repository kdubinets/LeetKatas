# Name

Unique Subsets with Same-Depth Duplicate Skipping

# Description

Return every distinct subset of the nondecreasing input exactly once, preserving the input. Each subset is nondecreasing, each input occurrence can be selected at most once, and the subsets are in lexicographic order. Empty input returns one empty subset.

Use emit-then-choose backtracking, skipping equal candidates only at the same depth and restoring the path after each branch. The learner implements the complete function and its recursive state.

This exercise covers same-depth duplicate suppression in sorted backtracking.

# Solution

```cpp
std::vector<std::vector<int>> result;
std::vector<int> path;
auto search = [&](auto&& self, std::size_t start) -> void {
    result.push_back(path);
    for (std::size_t index = start; index < sorted_values.size(); ++index) {
        if (index > start && sorted_values[index] == sorted_values[index - 1]) {
            continue;
        }
        path.push_back(sorted_values[index]);
        self(self, index + 1);
        path.pop_back();
    }
};
search(search, 0);
return result;
```
