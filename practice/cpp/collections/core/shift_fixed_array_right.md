# Name

Shift Fixed Array Right

# Description

Mutate a six-element integer array by discarding its last value, shifting the first five elements one position toward the end, and placing a supplied integer at the front. This exercise covers safe copying between overlapping ranges in the required direction.

# Solution

```cpp
std::copy_backward(values.begin(), values.end() - 1, values.end());
values.front() = new_front;
```
