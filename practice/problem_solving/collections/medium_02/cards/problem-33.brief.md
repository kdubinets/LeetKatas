# Search in Rotated Sorted Array

An array of **distinct** integers was sorted in increasing order and then
possibly rotated, moving some leading entries to the end without changing
their internal order. Given the resulting array and a target, return the
target's index, or `-1` if absent. Your running time must be `O(log n)`.

For example, `[0,1,2,4,5,6,7]` can become `[4,5,6,7,0,1,2]`, where the
target `0` is at index `4`. The array has between 1 and 5,000 elements;
values and the target lie between `-10^4` and `10^4`.
