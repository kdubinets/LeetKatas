# Name

Obtain Shared Ownership of Self

# Description

Complete `Node::owner` so it returns another `std::shared_ptr<Node>` sharing ownership of the current node. The node is guaranteed to have been created under existing shared ownership before this member is called. This exercise covers safe use of `std::enable_shared_from_this` without constructing a second control block.

# Solution

```cpp
return shared_from_this();
```
