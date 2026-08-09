# Name

Add Deque End Values

# Description

Mutate a `std::deque<int>` by placing `front_value` before its current first element and `back_value` after its current last element. Preserve the order of all existing values. This exercise covers efficient insertion at both ends of a deque.

# Solution

```cpp
values.push_front(front_value);
values.push_back(back_value);
```
