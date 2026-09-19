# Name

Manual First-Not-Less Binary Search

# Description

Return the first zero-based index where `values[i] >= target`, or `values.size()` if no such index exists. The input is sorted in nondecreasing order. For empty input, the result is zero.

The supplied pattern is manual lower-bound search. The answer remains between `low` and `high`, both inclusive: values before `low` are less than `target`, and values at or after `high` are not less than `target`. The unresolved values occupy `[low, high)`; when this interval becomes empty, `low == high` is the answer, possibly the one-past-end insertion position.

This exercise covers maintaining the lower-bound partition invariant in a half-open manual binary-search loop.

# Solution

```cpp
std::size_t low = 0;
std::size_t high = values.size();
while (low < high) {
    const std::size_t middle = low + (high - low) / 2;
    if (values[middle] < target) {
        low = middle + 1;
    } else {
        high = middle;
    }
}
return low;
```
