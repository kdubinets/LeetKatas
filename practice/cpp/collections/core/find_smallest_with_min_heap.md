# Name

Find Smallest with a Min-Heap

# Description

Given a nonempty const `std::vector<int>`, construct a priority-based container whose top is the smallest element and return that top value without modifying the input. This exercise covers configuring and constructing a min-heap.

# Solution

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap(
    values.begin(), values.end());
return min_heap.top();
```
