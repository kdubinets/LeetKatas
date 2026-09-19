# Name

Quickselect Range Shrinking with a Supplied Partition

# Description

Return the value at the valid zero-based rank in sorted order. Values may be rearranged, but size and multiplicities remain unchanged; duplicates are allowed.

The supplied partition helper places its last-element pivot at its final position. The quickselect invariant keeps an inclusive range containing the desired rank and discards the impossible side.

This exercise covers inclusive quickselect range maintenance from a supplied partition result.

# Solution

```cpp
std::size_t low = 0;
std::size_t high = values.size() - 1;
while (true) {
    const std::size_t pivot =
        partition_around_last(values, low, high);
    if (pivot == rank) {
        return values[pivot];
    }
    if (rank < pivot) {
        high = pivot - 1;
    } else {
        low = pivot + 1;
    }
}
```
