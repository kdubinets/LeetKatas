# Name

Union Two Distinct Roots by Size

# Description

Unite two distinct root components and return the surviving root: the root of the component with more vertices, or the original left_root if their sizes are equal. Parent is a valid rooted forest with roots pointing to themselves. The size array has the same length and accurate positive component sizes at roots; both supplied indices are valid distinct roots. Change only the losing root's parent and the surviving root's size, adding the losing component's size.

Use weighted root attachment to maintain the parent forest and accurate surviving-root size.

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
