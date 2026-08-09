# Name

Merge Unique Map Nodes

# Description

Transfer nodes from `source` into `destination` when their keys are not already present in the destination. Preserve destination values for collisions and leave every colliding source node in `source`; do not copy or move mapped strings. This exercise covers node-based merge between compatible ordered maps.

# Solution

```cpp
destination.merge(source);
```
