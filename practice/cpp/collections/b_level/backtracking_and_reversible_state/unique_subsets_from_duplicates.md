# Name

Unique Subsets with Same-Depth Duplicate Skipping

# Description

Append every distinct subset in depth-first lexicographic order from a nondecreasing input. Initial state is empty at index zero and input is preserved.

The supplied emit-then-choose search skips an equal candidate only when it repeats the preceding choice at the same depth, then restores the shared path.

This exercise covers same-depth duplicate suppression in sorted backtracking.

# Solution

```cpp
result.push_back(path);
for (std::size_t index = start; index < sorted_values.size(); ++index) {
    if (index > start && sorted_values[index] == sorted_values[index - 1]) {
        continue;
    }
    path.push_back(sorted_values[index]);
    collect_unique_subsets(sorted_values, index + 1, path, result);
    path.pop_back();
}
```
