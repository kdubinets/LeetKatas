# Name

Generate Fixed-Size Increasing Combinations

# Description

Append every length-k increasing combination from 1 through n in lexicographic order. The initial helper call has next one and empty state; k is valid. The wrapper returns all results, including one empty combination when k is zero.

The supplied search appends a candidate, recurses from its successor, restores the path, and prunes when insufficient values remain.

This exercise covers shared-path restoration around increasing recursive choices.

# Solution

```cpp
if (path.size() == k) {
    result.push_back(path);
    return;
}
const std::size_t needed = k - path.size();
for (std::size_t value = next; value <= n; ++value) {
    if (n - value + 1 < needed) {
        break;
    }
    path.push_back(value);
    collect_k_combinations(n, k, value + 1, path, result);
    path.pop_back();
}
```
