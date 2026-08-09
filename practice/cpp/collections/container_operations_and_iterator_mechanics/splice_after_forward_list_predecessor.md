# Name

Splice After Forward-List Predecessors

# Description

Transfer the existing node immediately after `source_predecessor` so it becomes the node immediately after `destination_predecessor`. The source and destination are distinct `std::forward_list<int>` objects; do not copy or move the element value. This exercise covers single-node predecessor-based transfer between forward lists.

# Solution

```cpp
destination.splice_after(destination_predecessor, source, source_predecessor);
```
