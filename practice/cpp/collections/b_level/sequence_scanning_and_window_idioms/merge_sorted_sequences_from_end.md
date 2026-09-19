# Name

Merge Sorted Sequences From the End

# Description

After the function returns, `left` must contain all original values from its first `left_count` elements and from `right`, in nondecreasing order, including duplicates. Both input sequences are sorted. The remaining original elements of `left` are output placeholders. Initially, `left.size()` equals `left_count + right.size()`, and its size must stay unchanged.

The supplied pattern is a backwards two-pointer merge whose completed output suffix does not overwrite unread values in the left input prefix.

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
