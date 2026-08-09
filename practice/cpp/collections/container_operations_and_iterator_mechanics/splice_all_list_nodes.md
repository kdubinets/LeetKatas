# Name

Splice All List Nodes

# Description

Transfer every node from `source` into `destination` immediately before `position`. The two lists are distinct. Preserve the order of both sequences, leave `source` empty, and do not copy or move element values. This exercise covers whole-list node transfer and stable iterators with `std::list`.

# Solution

```cpp
destination.splice(position, source);
```
