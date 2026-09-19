# Name

Permute Distinct Values with Used Markers

# Description

Append every permutation of distinct input values in input-index choice order. Initial used markers are false and path/result empty. Preserve values; empty input produces one empty permutation.

The supplied search marks one unused position, appends its value, recurses, then restores both path and marker.

This exercise covers coordinated restoration of a path and selected-position marker.

# Solution

```cpp
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
    collect_distinct_permutations(values, used, path, result);
    path.pop_back();
    used[index] = false;
}
```
