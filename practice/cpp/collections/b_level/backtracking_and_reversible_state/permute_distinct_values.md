# Name

Permute Distinct Values with Used Markers

# Description

Return every permutation of the distinct input values, preserving the input. Order results by the sequences of original input indices chosen, in lexicographic order; the values themselves need not be sorted. Empty input returns one empty permutation.

Use position-choice backtracking and restore both the current path and the selected-position marker after every branch. The learner implements the complete function and its recursive state.

This exercise covers coordinated restoration of a path and selected-position marker.

# Solution

```cpp
std::vector<std::vector<int>> result;
std::vector<int> path;
std::vector<bool> used(values.size(), false);
auto search = [&](auto&& self) -> void {
    if (path.size() == values.size()) {
        result.push_back(path);
        return;
    }
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (used[index]) {
            continue;
        }
        used[index] = true;
        path.push_back(values[index]);
        self(self);
        path.pop_back();
        used[index] = false;
    }
};
search(search);
return result;
```
