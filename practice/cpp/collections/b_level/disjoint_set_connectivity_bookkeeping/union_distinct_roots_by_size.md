# Name

Union Two Distinct Roots by Size

# Description

Unite two distinct roots and return the surviving root. Parent and size arrays align; both indices are roots with accurate positive component sizes. Only root parentage and the surviving size may change. On equal sizes, the original left root survives.

The supplied weighted attachment makes the larger root survive and adds the smaller component's size to it.

This exercise covers weighted attachment and surviving-root size maintenance.

# Solution

```cpp
if (component_size[left_root] < component_size[right_root]) {
    std::swap(left_root, right_root);
}
parent[right_root] = left_root;
component_size[left_root] += component_size[right_root];
return left_root;
```
