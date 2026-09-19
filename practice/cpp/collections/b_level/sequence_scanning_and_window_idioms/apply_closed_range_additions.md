# Name

Apply Closed Range Additions

# Description

Return a `std::vector<long long>` of length `size`. At each index, its value is the sum of `delta` from every update covering that index, or zero if no update covers it. Ranges include both endpoints, so overlapping additions accumulate. Indices are zero-based and every update satisfies `first <= last < size`.

The supplied pattern is a difference array: its boundary changes represent the updates, and its running total represents the accumulated value at each position.

This exercise covers difference-array boundary cancellation and running-total materialization for closed range updates.

# Solution

```cpp
std::vector<long long> differences(size + 1, 0);
for (const RangeAddition& update : updates) {
    differences[update.first] += update.delta;
    differences[update.last + 1] -= update.delta;
}

std::vector<long long> result(size);
long long current = 0;
for (std::size_t index = 0; index < size; ++index) {
    current += differences[index];
    result[index] = current;
}
return result;
```
