# Name

Merge K Sorted Sequences through a Heap Frontier

# Description

Return all values from the sorted input sequences in nondecreasing order, preserving duplicates. Inputs may be empty and are unchanged.

The supplied minimum heap contains one frontier entry per nonexhausted sequence. Emitting an entry exposes only its successor from the same sequence.

This exercise covers replacement of consumed multi-sequence heap-frontier entries.

# Solution

```cpp
using Entry = std::tuple<int, std::size_t, std::size_t>;
std::priority_queue<Entry, std::vector<Entry>, std::greater<>> frontier;
std::size_t total = 0;
for (std::size_t sequence = 0; sequence < sequences.size(); ++sequence) {
    total += sequences[sequence].size();
    if (!sequences[sequence].empty()) {
        frontier.emplace(sequences[sequence][0], sequence, 0);
    }
}
std::vector<int> result;
result.reserve(total);
while (!frontier.empty()) {
    const auto [value, sequence, position] = frontier.top();
    frontier.pop();
    result.push_back(value);
    const std::size_t next = position + 1;
    if (next < sequences[sequence].size()) {
        frontier.emplace(sequences[sequence][next], sequence, next);
    }
}
return result;
```
