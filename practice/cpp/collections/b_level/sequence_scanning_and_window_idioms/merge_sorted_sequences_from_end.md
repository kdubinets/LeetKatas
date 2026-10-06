# Name

Merge Sorted Sequences From the End

# Description

Fill left with all original values from its first left_count elements and from right in nondecreasing order, including duplicates. The first left_count elements of left and all of right are sorted; remaining left elements are placeholders with arbitrary values. The vectors are distinct. Leave right unchanged and preserve left.size(), initially left_count + right.size().

Use a backwards two-pointer merge so the completed output suffix never overwrites unread values in the left input prefix. The learner implements the complete entry function.

This exercise covers merging sorted sequences backwards into reserved output space without overwriting unread input values.

# Solution

```cpp
std::size_t write = left.size();
std::size_t left_index = left_count;
std::size_t right_index = right.size();
while (right_index > 0) {
    if (left_index > 0 && left[left_index - 1] > right[right_index - 1]) {
        left[--write] = left[--left_index];
    } else {
        left[--write] = right[--right_index];
    }
}
```
