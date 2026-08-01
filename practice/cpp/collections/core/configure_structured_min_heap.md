# Name

Configure Structured Min-Heap

# Description

Complete the comparator used by a priority queue of tasks so its top task has the lowest integer priority, breaking ties by the lowest integer ID. The comparator must define a valid strict weak ordering. This exercise covers the reversed ordering convention of a structured min-heap comparator.

# Solution

```cpp
if (left.priority != right.priority) {
    return left.priority > right.priority;
}
return left.id > right.id;
```
