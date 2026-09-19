# Name

Longest Common Subsequence with a Rolling Row

# Description

Return the greatest length of a byte sequence that appears in both inputs in the same relative order; selected bytes need not be contiguous. Empty input gives zero. Inputs are read-only string views.

The supplied two-sequence dynamic-programming recurrence uses one in-place row. Before a cell is overwritten, its prior-row value is retained as the next diagonal. Equal bytes extend the prior diagonal; unequal bytes take the maximum of the prior-row and current-row neighbors.

This exercise covers in-place two-sequence row updates with preservation of the overwritten diagonal.

# Solution

```cpp
std::vector<std::size_t> lengths(second.size() + 1, 0);
for (char left : first) {
    std::size_t diagonal = 0;
    for (std::size_t column = 1; column <= second.size(); ++column) {
        const std::size_t prior_row = lengths[column];
        if (left == second[column - 1]) {
            lengths[column] = diagonal + 1;
        } else {
            lengths[column] = std::max(lengths[column], lengths[column - 1]);
        }
        diagonal = prior_row;
    }
}
return lengths.back();
```
