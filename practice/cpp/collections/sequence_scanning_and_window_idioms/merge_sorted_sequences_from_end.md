# Name

Merge Sorted Sequences From the End

# Description

Use a backwards two-pointer merge to combine the ascending prefix of `left` and ascending `right` into `left`. `left_count` is the number of initialized values in `left`, and `left.size()` equals `left_count + right.size()`. Filling from the end preserves unread values in the left prefix.

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
