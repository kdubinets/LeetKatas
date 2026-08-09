# Name

Take Deque End Values

# Description

Given a `std::deque<int>` containing at least two elements, return its current first and last values as a pair and remove those two elements. Every interior element must remain in its original order. This exercise covers paired access and removal at both deque endpoints.

# Solution

```cpp
std::pair result{values.front(), values.back()};
values.pop_front();
values.pop_back();
return result;
```
